"""
Per-key sanity-check validators for ChecklistItem values.

The sync mgmt command and the new `recheck_sanity` command both dispatch to
this module. Each validator inspects a value (plus optional cross-field
context: basic shares, diluted, prior period, etc.) and returns a
SanityResult with severity:

  - ERROR:   data is wrong (negative, out-of-band, missing required parts).
             Blocks publication. sanity_check_passed=False.
  - WARNING: data is suspicious — possible mis-extraction or unusual
             corporate event. Blocks publication; can be resolved by
             human review/waiver. sanity_check_passed=False.
  - INFO:    informational note. sanity_check_passed=True (doesn't block).
  - PASS:    clean. sanity_check_passed=True.

Severity tag is prefixed to the notes string for ops visibility, e.g.
'[WARNING] diluted/basic ratio 0.96 — slightly below 1.0; check for buybacks'.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional


SEVERITY_ERROR   = "ERROR"
SEVERITY_WARNING = "WARNING"
SEVERITY_INFO    = "INFO"


@dataclass
class SanityResult:
    passed: bool
    severity: str
    notes: str

    def with_prefix(self) -> str:
        if not self.notes:
            return f"[{self.severity}]"
        return f"[{self.severity}] {self.notes}"


def _ok() -> SanityResult:
    return SanityResult(True, SEVERITY_INFO, "")


def _error(notes: str) -> SanityResult:
    return SanityResult(False, SEVERITY_ERROR, notes)


def _warning(notes: str) -> SanityResult:
    return SanityResult(False, SEVERITY_WARNING, notes)


# ─────────────────────────── helpers ───────────────────────────

def _parse_filing_date(local_path: str) -> Optional[datetime]:
    """Extract YYYYMMDD from a filename like 'mda-20260421.pdf'."""
    if not local_path:
        return None
    m = re.search(r"(\d{4})(\d{2})(\d{2})", local_path)
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
    except ValueError:
        return None


def _filing_age_days(local_path: str) -> Optional[int]:
    d = _parse_filing_date(local_path)
    if d is None:
        return None
    return (datetime.now(timezone.utc) - d).days


# ─────────────────────────── validators ───────────────────────────

# Plausibility band for a public-company common-share count.
_MIN_SHARES = 100_000          # Below this is suspicious (penny shell?)
_MAX_SHARES = 10_000_000_000   # Above this is suspicious (Apple-level)


def check_shares_issued_outstanding(value, *, prior_value=None, **_) -> SanityResult:
    """Basic count must be a positive integer in a plausible band, with
    sanity around year-over-year change."""
    try:
        v = int(value)
    except (TypeError, ValueError):
        return _error(f"non-integer value: {value!r}")
    if v <= 0:
        return _error(f"non-positive count: {v}")
    if v < _MIN_SHARES:
        return _warning(f"unusually low: {v:,} (possible mis-extraction)")
    if v > _MAX_SHARES:
        return _warning(f"unusually high: {v:,} (possible mis-extraction)")

    # YoY outlier — defends against the "Sandstorm 28.7M" extraction bug
    # where one tranche was mistaken for total outstanding
    if prior_value is not None:
        try:
            prev = int(prior_value)
            if prev > 0:
                ratio = v / prev
                if ratio > 5.0:
                    return _warning(
                        f"basic shares grew {ratio:.1f}x vs. prior period "
                        f"({prev:,} → {v:,}) — verify a corporate action explains this"
                    )
                if ratio < 0.2:
                    return _warning(
                        f"basic shares dropped to {ratio:.1f}x vs. prior period "
                        f"({prev:,} → {v:,}) — verify a consolidation or buyback explains this"
                    )
        except (TypeError, ValueError):
            pass
    return _ok()


def check_shares_fully_diluted(value, *, basic=None, **_) -> SanityResult:
    """Diluted must equal basic + sum-of-instruments, give or take. Ratio
    bounded between 1.0x and 2.0x (above 2x is unusual heavy warrant
    overhang; below 1.0x is impossible)."""
    try:
        v = int(value)
        b = int(basic) if basic else None
    except (TypeError, ValueError):
        return _error(f"non-integer value(s): diluted={value!r} basic={basic!r}")
    if v <= 0:
        return _error(f"non-positive diluted count: {v}")
    if b is None:
        return _error("basic shares not available — cannot validate ratio")
    if b <= 0:
        return _error(f"basic shares non-positive: {b}")
    ratio = v / b
    if ratio < 0.95:
        return _error(f"diluted ({v:,}) less than basic ({b:,}) — ratio {ratio:.2f}")
    if ratio < 1.0:
        return _warning(f"diluted slightly below basic — ratio {ratio:.3f}; check for buybacks")
    if ratio > 3.0:
        return _warning(f"diluted/basic ratio {ratio:.2f}x — extreme overhang; verify warrants/options counts")
    if ratio > 2.0:
        return _warning(f"diluted/basic ratio {ratio:.2f}x — heavy overhang; double-check extraction")
    return _ok()


def check_share_instruments(value, *, basic=None, diluted=None, **_) -> SanityResult:
    """Instrument list must reconcile against (diluted − basic) gap."""
    if not isinstance(value, list):
        return _error(f"value is not a list (got {type(value).__name__})")
    # Per-tranche shape checks
    valid_types = {"warrant", "option", "flow_through"}
    for i, tranche in enumerate(value):
        if not isinstance(tranche, dict):
            return _error(f"tranche {i} is not a dict")
        t = (tranche.get("type") or "").lower()
        if t not in valid_types:
            return _error(f"tranche {i} has invalid type: {tranche.get('type')!r}")
        try:
            int(tranche.get("count") or 0)
        except (TypeError, ValueError):
            return _error(f"tranche {i} count is not an integer: {tranche.get('count')!r}")

    # Reconciliation
    if basic is None or diluted is None:
        return _warning("cannot reconcile without basic and diluted counts")
    try:
        total = sum(int(t.get("count") or 0) for t in value)
        gap = int(diluted) - int(basic)
    except (TypeError, ValueError):
        return _error("non-integer in instrument counts or basic/diluted")
    if gap == 0:
        if total > 0:
            return _warning(f"instruments total {total:,} but diluted == basic")
        return _ok()
    pct = abs(total - gap) / gap
    if pct > 0.10:
        return _warning(f"instruments {total:,} vs. (diluted-basic) gap {gap:,} differ by {pct:.1%}")
    if pct > 0.05:
        return SanityResult(True, SEVERITY_INFO, f"instruments-gap reconciliation: {pct:.1%} mismatch (within tolerance)")
    return _ok()


def check_mda_recency(value, **_) -> SanityResult:
    """MD&A must be within 180 days (1 quarter + grace)."""
    if not isinstance(value, dict):
        return _error("value is not a dict")
    path = (value.get("date") or "") + ".pdf"
    age = _filing_age_days(path) if value.get("date") else None
    if age is None:
        return _error("could not parse filing date from value")
    if age > 540:  # 18 months — definitely stale, likely abandoned
        return _error(f"filing is {age} days old (>540 — likely stale/abandoned)")
    if age > 180:
        return _warning(f"filing is {age} days old (>180 — needs re-harvest)")
    return _ok()


def check_financials_recency(value, **_) -> SanityResult:
    """Annual financials within 18 months."""
    if not isinstance(value, dict):
        return _error("value is not a dict")
    path = (value.get("date") or "") + ".pdf"
    age = _filing_age_days(path) if value.get("date") else None
    if age is None:
        return _error("could not parse filing date")
    if age > 540:
        return _error(f"audited financials are {age} days old (>18 months)")
    if age > 450:
        return _warning(f"audited financials are {age} days old (approaching 18-month limit)")
    return _ok()


# Resource-row pattern: should look like
#   "Indicated 2,520 3.16 0.91 256 74 5,281 7.10 2.19 1,205 311 ..."
# i.e., a category word followed by 3+ numeric tokens.
_RESOURCE_ROW_RE = re.compile(
    r"^(meas|measured|ind|indicated|inf|inferred|m\&i|pro|proven|prob|probable|p\+p)",
    re.I,
)
_TOC_LEADER_RE = re.compile(r"\.{4,}")


def check_resource_row(value, **_) -> SanityResult:
    """Verbatim resource/reserve table row must look like a data row, not
    TOC garbage or prose."""
    if value in (None, ""):
        return SanityResult(True, SEVERITY_INFO, "field is null (acceptable for pre-resource explorers; waive if so)")
    if not isinstance(value, str):
        return _error(f"value is not a string (got {type(value).__name__})")
    s = value.strip()
    if _TOC_LEADER_RE.search(s):
        return _error("contains dot-leaders (looks like a table-of-contents entry)")
    if not _RESOURCE_ROW_RE.match(s):
        return _warning(f"does not start with a category word: {s[:60]!r}")
    nums = re.findall(r"\d", s)
    if len(nums) < 3:
        return _error(f"too few digits for a resource row: {s[:60]!r}")
    return _ok()


def check_43101_status(value, **_) -> SanityResult:
    """Latest 43-101 must exist and be plausibly recent. No max-age cap
    (5-year-old 43-101 can still be authoritative)."""
    if value is None or value == {}:
        return _warning("no 43-101 in cache; explorer may legitimately have no resource estimate yet")
    if not isinstance(value, dict):
        return _error("value is not a dict")
    if not value.get("local_path"):
        return _error("local_path missing from 43-101 source record")
    return _ok()


def check_aif(value, **_) -> SanityResult:
    """AIF is optional (junior issuers commonly don't file)."""
    if value is None:
        return _ok()
    if not isinstance(value, dict):
        return _error("value is not a dict")
    path = (value.get("date") or "") + ".pdf"
    age = _filing_age_days(path) if value.get("date") else None
    if age is not None and age > 540:
        return _warning(f"AIF is {age} days old; junior may have stopped filing AIFs")
    return _ok()


def check_recent_material_event(value, **_) -> SanityResult:
    if value is None:
        return _ok()  # RECOMMENDED, not REQUIRED
    return _ok()  # placeholder until material-event extractor lands


def check_insider_activity_90d(value, **_) -> SanityResult:
    if value is None:
        return _ok()  # RECOMMENDED — silent absence is OK
    return _ok()  # placeholder until CI scraper completes


# ─────────────────────── registry + dispatcher ───────────────────────

_VALIDATORS = {
    "shares_issued_outstanding": check_shares_issued_outstanding,
    "shares_fully_diluted":      check_shares_fully_diluted,
    "share_instruments":         check_share_instruments,
    "mda_annual_or_interim":     check_mda_recency,
    "financials_annual":         check_financials_recency,
    "resource_or_43101_status":  check_43101_status,
    "aif":                       check_aif,
    "recent_material_event":     check_recent_material_event,
    "insider_activity_90d":      check_insider_activity_90d,
}


def validate(key: str, value: Any, **ctx) -> SanityResult:
    """Dispatch by key. Unknown keys get a free pass (no validator yet)."""
    fn = _VALIDATORS.get(key)
    if fn is None:
        return SanityResult(True, SEVERITY_INFO, f"no validator registered for {key!r}")
    return fn(value, **ctx)
