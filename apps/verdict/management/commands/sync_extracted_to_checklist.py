"""
Sync the laptop harvester's extracted/<TICKER>.json files into the
ChecklistItem + CompanyHarvestState models.

Runs on the droplet (where the Django DB lives). Idempotent — safe to
re-run; values get updated in place.

What it does, per ticker JSON:
  - Reads research_queue/extracted/<TICKER>.json (from the repo working tree)
  - Maps each extracted field to a ChecklistItem row (auto-filled)
  - Records provenance (sha256 + filing date + path)
  - Runs inline sanity-check rules; sets sanity_check_passed
  - Aggregates into CompanyHarvestState (status, blockers_summary,
    ready_for_verdict, last_successful_harvest)

Doesn't fetch anything from the network. Pure file -> DB transform.
"""
import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone as djtz

from apps.verdict.models import (
    Company, CompanyHarvestState, HarvestStateChoice,
    ChecklistItem, ChecklistItemCategory, ChecklistItemStatus,
    ChecklistItemSource,
)


EXTRACTED_DIR = Path(__file__).resolve().parents[4] / "research_queue" / "extracted"


# ────────────────────── sanity-check engine ─────────────────────

def _sanity_shares_outstanding(value):
    try:
        v = int(value)
    except (TypeError, ValueError):
        return False, "non-integer value"
    if not (1_000_000 <= v <= 10_000_000_000):
        return False, f"out of plausible band: {v:,}"
    return True, ""


def _sanity_shares_fully_diluted(value, basic):
    try:
        v = int(value)
        b = int(basic) if basic else None
    except (TypeError, ValueError):
        return False, "non-integer value"
    if b is None or b <= 0:
        return False, "basic shares not set; cannot validate ratio"
    ratio = v / b
    if not (1.0 <= ratio <= 2.0):
        return False, f"diluted/basic ratio {ratio:.2f} out of 1.0-2.0 band"
    return True, ""


def _sanity_share_instruments(instruments, basic, diluted):
    if not isinstance(instruments, list):
        return False, "value is not a list"
    if not basic or not diluted:
        return False, "cannot validate without basic and diluted counts"
    try:
        total = sum(int(i.get("count") or 0) for i in instruments)
        gap = int(diluted) - int(basic)
    except (TypeError, ValueError):
        return False, "non-integer count in instruments"
    if gap == 0:
        # Companies with no warrants/options can legitimately have diluted == basic
        return total == 0, "" if total == 0 else f"instruments total {total} but diluted == basic"
    pct = abs(total - gap) / gap
    if pct > 0.05:
        return False, f"instrument sum {total:,} vs (diluted-basic) gap {gap:,} differ by {pct:.1%}"
    return True, ""


def _sanity_filing_recent(local_path, days_limit):
    """Filing date is encoded in the path as YYYYMMDD."""
    if not local_path:
        return False, "no source filing path"
    import re
    m = re.search(r"(\d{4})(\d{2})(\d{2})", local_path)
    if not m:
        return False, "could not parse filing date from path"
    try:
        filing_date = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
    except ValueError:
        return False, "invalid filing date"
    age_days = (datetime.now(timezone.utc) - filing_date).days
    if age_days > days_limit:
        return False, f"filing is {age_days} days old (limit {days_limit})"
    return True, ""


# ────────────────────── per-ticker sync ─────────────────────

def _upsert_item(company, key, *, value=None, source_type="", source_ref="",
                  source_page=None, status=ChecklistItemStatus.AUTO_FILLED,
                  sanity_passed=False, sanity_notes="", updated_by="sync_extracted"):
    obj, _ = ChecklistItem.objects.get_or_create(
        company=company, key=key,
        defaults={"category": ChecklistItemCategory.REQUIRED},
    )
    obj.value = value
    obj.source_type = source_type
    obj.source_ref = source_ref
    obj.source_page = source_page
    obj.status = status
    obj.sanity_check_passed = sanity_passed
    obj.sanity_check_notes = sanity_notes
    obj.updated_by = updated_by
    obj.save()
    return obj


def _sync_ticker(data: dict) -> tuple[int, list]:
    """Returns (items_touched, list_of_failed_keys)."""
    ticker = (data.get("ticker") or "").upper().strip()
    if not ticker:
        return 0, []
    try:
        company = Company.objects.get(ticker__iexact=ticker)
    except Company.DoesNotExist:
        return 0, [f"company '{ticker}' not in DB"]

    touched = 0
    failures: list[str] = []
    sources = data.get("sources") or {}
    cap_src = sources.get("cap_table_source") or {}
    tech_src = sources.get("tech_43101_source") or {}
    fin_src = sources.get("financials_annual_source") or {}
    aif_src = sources.get("aif_source") or {}

    # ── mda_annual_or_interim ──
    if cap_src.get("local_path"):
        ok, notes = _sanity_filing_recent(cap_src["local_path"], 180)
        _upsert_item(
            company, "mda_annual_or_interim",
            value={"bucket": cap_src.get("bucket"), "date": cap_src.get("date")},
            source_type=ChecklistItemSource.SEDAR_HARVESTER,
            source_ref=cap_src.get("sha256") or "",
            status=ChecklistItemStatus.AUTO_FILLED,
            sanity_passed=ok,
            sanity_notes=notes,
        )
        touched += 1

    # ── shares_issued_outstanding ──
    basic = data.get("shares_issued_outstanding")
    if basic is not None:
        ok, notes = _sanity_shares_outstanding(basic)
        _upsert_item(
            company, "shares_issued_outstanding",
            value=basic,
            source_type=ChecklistItemSource.SEDAR_HARVESTER,
            source_ref=cap_src.get("sha256") or "",
            status=ChecklistItemStatus.AUTO_FILLED,
            sanity_passed=ok,
            sanity_notes=notes,
        )
        touched += 1
    else:
        _upsert_item(
            company, "shares_issued_outstanding",
            status=ChecklistItemStatus.FAILED,
            sanity_notes="extractor returned null",
        )
        failures.append("shares_issued_outstanding")
        touched += 1

    # ── shares_fully_diluted ──
    diluted = data.get("shares_fully_diluted")
    if diluted is not None:
        ok, notes = _sanity_shares_fully_diluted(diluted, basic)
        _upsert_item(
            company, "shares_fully_diluted",
            value=diluted,
            source_type=ChecklistItemSource.SEDAR_HARVESTER,
            source_ref=cap_src.get("sha256") or "",
            status=ChecklistItemStatus.AUTO_FILLED,
            sanity_passed=ok,
            sanity_notes=notes,
        )
        touched += 1
    else:
        _upsert_item(
            company, "shares_fully_diluted",
            status=ChecklistItemStatus.FAILED,
            sanity_notes="extractor returned null",
        )
        failures.append("shares_fully_diluted")
        touched += 1

    # ── share_instruments ──
    instruments = data.get("share_instruments") or []
    ok, notes = _sanity_share_instruments(instruments, basic, diluted)
    _upsert_item(
        company, "share_instruments",
        value=instruments,
        source_type=ChecklistItemSource.SEDAR_HARVESTER,
        source_ref=cap_src.get("sha256") or "",
        status=ChecklistItemStatus.AUTO_FILLED if instruments else ChecklistItemStatus.FAILED,
        sanity_passed=ok,
        sanity_notes=notes,
    )
    if not instruments:
        failures.append("share_instruments")
    touched += 1

    # ── resource_or_43101_status ──
    if tech_src.get("local_path"):
        _upsert_item(
            company, "resource_or_43101_status",
            value={"date": tech_src.get("date"), "local_path": tech_src.get("local_path")},
            source_type=ChecklistItemSource.SEDAR_HARVESTER,
            source_ref=tech_src.get("sha256") or "",
            status=ChecklistItemStatus.AUTO_FILLED,
            sanity_passed=True,
            sanity_notes="",
        )
        touched += 1

    # ── financials_annual ──
    # We don't extract structured fields from the financials yet, but its
    # mere presence in the cache (within an 18-month window) is enough to
    # satisfy the checklist row.
    if fin_src.get("local_path"):
        ok, notes = _sanity_filing_recent(fin_src["local_path"], 18 * 30)
        _upsert_item(
            company, "financials_annual",
            value={"bucket": fin_src.get("bucket"), "date": fin_src.get("date")},
            source_type=ChecklistItemSource.SEDAR_HARVESTER,
            source_ref=fin_src.get("sha256") or "",
            status=ChecklistItemStatus.AUTO_FILLED,
            sanity_passed=ok,
            sanity_notes=notes,
        )
        touched += 1

    # ── aif (OPTIONAL — does not block) ──
    if aif_src.get("local_path"):
        ok, notes = _sanity_filing_recent(aif_src["local_path"], 18 * 30)
        _upsert_item(
            company, "aif",
            value={"bucket": aif_src.get("bucket"), "date": aif_src.get("date")},
            source_type=ChecklistItemSource.SEDAR_HARVESTER,
            source_ref=aif_src.get("sha256") or "",
            status=ChecklistItemStatus.AUTO_FILLED,
            sanity_passed=ok,
            sanity_notes=notes,
        )
        touched += 1

    return touched, failures


# ────────────────────── harvest state aggregation ─────────────────────

def _refresh_harvest_state(company):
    """Recompute CompanyHarvestState fields from current ChecklistItem rows."""
    state, _ = CompanyHarvestState.objects.get_or_create(company=company)
    required = list(company.checklist_items.filter(category=ChecklistItemCategory.REQUIRED))
    unsatisfied = [
        item for item in required
        if not item.is_satisfied
    ]
    state.ready_for_verdict = (len(unsatisfied) == 0)
    state.blockers_summary = "; ".join(
        f"{i.key}({i.get_status_display()})" for i in unsatisfied
    )[:1500]
    if state.ready_for_verdict:
        state.status = HarvestStateChoice.READY
    else:
        state.status = HarvestStateChoice.BLOCKED
    state.last_successful_harvest = djtz.now()
    state.save()
    return state


# ────────────────────── command ─────────────────────

class Command(BaseCommand):
    help = "Sync extracted-JSON files into ChecklistItem + CompanyHarvestState."

    def add_arguments(self, parser):
        parser.add_argument(
            "--tickers", nargs="*", default=None,
            help="Limit to specific tickers (default: all JSON files).",
        )
        parser.add_argument(
            "--dir", default=str(EXTRACTED_DIR),
            help="Directory containing extracted/<TICKER>.json files.",
        )

    def handle(self, *args, **opts):
        d = Path(opts["dir"])
        if not d.is_dir():
            self.stderr.write(f"directory not found: {d}")
            return

        files = sorted(d.glob("*.json"))
        if opts["tickers"]:
            wanted = {t.upper() for t in opts["tickers"]}
            files = [f for f in files if f.stem.upper() in wanted]

        n_tickers = 0
        n_ready   = 0
        n_blocked = 0
        for f in files:
            try:
                data = json.loads(f.read_text())
            except Exception as e:
                self.stderr.write(f"{f.name}: parse error {e}")
                continue
            touched, failures = _sync_ticker(data)
            if touched == 0:
                continue
            try:
                company = Company.objects.get(ticker__iexact=data["ticker"])
            except Company.DoesNotExist:
                continue
            state = _refresh_harvest_state(company)
            n_tickers += 1
            if state.ready_for_verdict:
                n_ready += 1
            else:
                n_blocked += 1
            tag = "READY" if state.ready_for_verdict else "BLOCKED"
            self.stdout.write(
                f"  {company.ticker:6s}  {tag}  touched={touched}  "
                f"failures={','.join(failures) if failures else '-'}"
            )

        self.stdout.write(self.style.SUCCESS(
            f"Synced {n_tickers} tickers: {n_ready} ready, {n_blocked} blocked."
        ))
