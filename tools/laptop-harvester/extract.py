"""
Extract structured cap-table and resource fields from cached SEDAR+ filings
into JSON the hosted research-agent can read directly via git.

Layout written:
    research_queue/extracted/<TICKER>.json

Schema:
{
  "ticker": "AMX",
  "extracted_at": "2026-05-04T11:00:00Z",
  "sources": {
    "mda": {"local_path": "...", "sha256": "..."},
    "tech_43101": [{"local_path": "...", "sha256": "...", "date": "..."}, ...]
  },
  "shares_issued_outstanding": int | null,
  "shares_fully_diluted": int | null,
  "share_instruments": [{"type": "warrant"|"option", "count": int, "strike_price": float|null, "expiry": "YYYY-MM-DD"|null, "raw": "..."}],
  "resource_measured": str | null,
  "resource_indicated": str | null,
  "resource_inferred": str | null,
  "reserve_proven": str | null,
  "reserve_probable": str | null,
  "extraction_notes": [str, ...]   # what we tried, what we couldn't find
}

Run:
    python extract.py <TICKER>
    python extract.py --all
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pypdf

CACHE_ROOT = Path.home() / "sedar-cache"
OUT_DIR = Path.home() / "miningstockreport" / "research_queue" / "extracted"


# ---------- pdf helpers ----------

def _page_texts(pdf_path: Path, max_pages: int | None = None) -> list[str]:
    """Return per-page text, optionally capped to first N pages."""
    out = []
    try:
        r = pypdf.PdfReader(str(pdf_path))
        total = len(r.pages)
        n = total if max_pages is None else min(total, max_pages)
        for i in range(n):
            try:
                out.append(r.pages[i].extract_text() or "")
            except Exception:
                out.append("")
        return out
    except Exception as e:
        return []


def _last_pages(pdf_path: Path, n: int = 30) -> list[tuple[int, str]]:
    """Return [(page_idx, text), ...] for the last n pages of a PDF."""
    try:
        r = pypdf.PdfReader(str(pdf_path))
        total = len(r.pages)
        start = max(0, total - n)
        out = []
        for i in range(start, total):
            try:
                out.append((i, r.pages[i].extract_text() or ""))
            except Exception:
                out.append((i, ""))
        return out
    except Exception:
        return []


def _first_pages_with_keyword(pdf_path: Path, keyword: str,
                              search_pages: int = 60) -> list[tuple[int, str]]:
    """Find pages within first N that contain keyword (case-insensitive)."""
    out = []
    try:
        r = pypdf.PdfReader(str(pdf_path))
        n = min(len(r.pages), search_pages)
        for i in range(n):
            try:
                t = r.pages[i].extract_text() or ""
            except Exception:
                t = ""
            if keyword.lower() in t.lower():
                out.append((i, t))
        return out
    except Exception:
        return []


# ---------- cap table extraction ----------

# Numbers like 12,345,678 or 12 345 678 (French/Canadian style with NBSP) or 12345678
# Need to match digit-group separators that are: comma, regular space, or non-breaking space.
_LARGE_INT = re.compile(r"(\d{1,3}(?:[  ,]\d{3}){2,}|\d{6,})")


def _to_int(s: str) -> int | None:
    try:
        return int(re.sub(r"[\s, ]", "", s))
    except Exception:
        return None


def _extract_share_count(text: str, anchor_re: re.Pattern, window: int = 350) -> int | None:
    """Find anchor in text, return the largest plausible integer within window chars."""
    cands = []
    for m in anchor_re.finditer(text):
        seg = text[max(0, m.start() - window): m.end() + window]
        for nm in _LARGE_INT.finditer(seg):
            v = _to_int(nm.group(1))
            # Plausible share-count band: 1M - 10B
            if v and 1_000_000 <= v <= 10_000_000_000:
                cands.append(v)
    return max(cands) if cands else None


_ISSUED_OUTSTANDING = re.compile(
    r"(?:common\s+shares?\s+(?:issued\s+and\s+)?outstanding"
    r"|issued\s+and\s+outstanding\s+(?:common\s+)?shares?"
    r"|shares?\s+issued\s+and\s+outstanding"
    r"|securities\s+outstanding"
    r"|outstanding\s+share\s+information"
    r"|actions\s+ordinaires"        # French-Canadian common shares
    r"|actions\s+en\s+circulation)",  # French-Canadian shares outstanding
    re.I,
)
_FULLY_DILUTED = re.compile(r"(?:fully\s+diluted|sur\s+une\s+base\s+(?:enti[èe]rement\s+)?dilu[ée]e)", re.I)


_DIRECT_OUTSTANDING = [
    # "X [Company] common shares issued and outstanding" — allow 0-3 words between
    # number and 'common shares' so Barrick-style "1,675,360,395 Barrick common shares"
    # still matches.
    re.compile(r"(\d{1,3}(?:[ ,]\d{3}){2,})\s+(?:\w+\s+){0,3}common\s+shares?\s+(?:were\s+|are\s+)?(?:issued\s+and\s+)?outstanding", re.I),
    # "common shares issued and outstanding: X"
    re.compile(r"common\s+shares?\s+(?:issued\s+and\s+)?outstanding[\s:.]+(\d{1,3}(?:[ ,]\d{3}){2,})", re.I),
    # "shares issued and outstanding: X"
    re.compile(r"shares?\s+issued\s+and\s+outstanding[\s:.]+(\d{1,3}(?:[ ,]\d{3}){2,})", re.I),
    # BCM-style: "Issued and outstanding shares X" — different word order, label
    # leads with "Issued and outstanding", number follows the word "shares".
    re.compile(r"issued\s+and\s+outstanding\s+(?:common\s+)?shares?[\s:.]+(\d{1,3}(?:[ ,]\d{3}){2,})", re.I),
]


def _line_match_outstanding(text: str) -> int | None:
    """
    Line-by-line scan: find a SHORT (tabular) line with 'common shares' /
    'actions ordinaires' that is NOT also about diluted/warrants/options/
    insider holdings/etc. Robust against tabular bilingual layouts (e.g.,
    AMX's MD&A) but resists Barrick-style prose like
    'control or direction over 4,253,457 common shares' on a long line.
    """
    # Excludes prose lines that LOOK like a table row but are actually
    # narrative content. Two categories:
    #   (a) lines about other instruments (diluted/warrants/options/reserved)
    #   (b) lines about specific issuance events, financial-statement line
    #       items, or insider holdings — matched BCM's "Common shares issued
    #       (28,767,399) ... with a fair value of $4.1 million" wrongly because
    #       the original list missed financial-statement vocabulary.
    excl = re.compile(
        r"\b(diluted?|dilu[ée]e?s?|warrant|bons|option|total|reserved|reserve"
        r"|directly|indirectly|control|direction|exercise|holder|representing"
        r"|owned|held"
        # Financial-statement / specific-issuance prose:
        r"|fair\s+value|consideration|issuance|issued\s+to|issued\s+in"
        r"|restructuring|agreement|settlement|valuation|gain|loss"
        r"|expense|income|revenue|cost|liability|asset"
        r")\b",
        re.I,
    )
    label = re.compile(
        r"\b(actions\s+ordinaires|common\s+shares?"
        r"|issued\s+and\s+outstanding\s+(?:common\s+)?shares?)\b",
        re.I,
    )
    for line in text.split("\n"):
        if len(line) > 90:               # prose, not a table row
            continue
        if not label.search(line):
            continue
        if excl.search(line):
            continue
        m = _LARGE_INT.search(line)
        if not m:
            continue
        v = _to_int(m.group(1))
        if v and 1_000_000 <= v <= 10_000_000_000:
            return v
    return None


# Vocabulary that disqualifies a line from being a real cap-table row.
# Financial-statement / fair-value / theoretical-cap language. The 969M-warrant
# bug on BCM came from "Gain (loss) on valuation of warrant liability 969,638,331";
# the bogus 33M options came from "Options allowed 22,773,079" + "Shares reserved...".
_INSTRUMENT_LINE_EXCLUDE = re.compile(
    r"\b(fair\s+value|valuation|liability|gain|loss|expense|income"
    r"|revenue|cost|provision|adjustment|change\s+in"
    r"|allowed|reserved|reserve|granted|available|limit"
    r"|consideration|issuance|restructuring|agreement|fully\s+diluted)\b",
    re.I,
)
_SHARES_LINE_EXCLUDE = re.compile(
    r"\b(common\s+shares?|actions\s+ordinaires)\b",
    re.I,
)
_WARR_KW = re.compile(r"\b(warrants?|bons\s+de\s+souscription)\b", re.I)
_OPT_KW = re.compile(r"\b(stock[\s-]?options?|options?\s+d['’]?achat|options?\s+outstanding|^\s*options?\b)\b", re.I)
_OUTSTANDING_KW = re.compile(r"\boutstanding\b", re.I)


def _extract_instrument_counts(text: str) -> tuple[int, int]:
    """
    Return (warrants_outstanding, options_outstanding) by finding the
    cap-table summary row for each. Per-line scan with strong exclusions:
        1. Skip lines with financial-statement vocabulary (fair value, gain,
           loss, liability, valuation, etc.) — fixes the BCM bug.
        2. Skip lines about plan caps, reserves, grants ("allowed", "reserved",
           "granted") — these are theoretical, not outstanding.
        3. Skip lines that are clearly the COMMON-SHARES row (otherwise the
           AMX bilingual-table pattern would match the common-shares line for
           warrants too).
        4. Prefer lines containing "outstanding" (most explicit signal).
           Fall through to any other unfiltered line if no "outstanding"
           match exists (handles AMX-style label-number-label tabular).
        5. Pick the smallest plausible candidate (overcounting is the more
           common failure mode; a single warrant-tranche figure is typically
           smaller than a fair-value-adjustment figure).
    Returns (0, 0) if no anchored match found — better to be silent than wrong.
    """
    def _scan(want_re: re.Pattern, exclude_others: re.Pattern) -> int:
        with_outstanding: list[int] = []
        without: list[int] = []
        for line in text.split("\n"):
            if len(line) > 200:
                continue
            if not want_re.search(line):
                continue
            if exclude_others.search(line):
                continue
            if _INSTRUMENT_LINE_EXCLUDE.search(line):
                continue
            if _SHARES_LINE_EXCLUDE.search(line):
                # Bilingual lines like "Bons de souscription 1 979 750 Warrants"
                # don't have "common shares" but we still want them; only skip
                # if the line is clearly about common shares specifically.
                # This regex matches both "common shares" and the row label —
                # but in AMX's table, the warrant line says only "Warrants",
                # not "Common shares", so it passes. Keep this rule.
                continue
            m = _LARGE_INT.search(line)
            if not m:
                continue
            v = _to_int(m.group(1))
            if not v or v < 1_000 or v > 1_000_000_000:
                continue
            if _OUTSTANDING_KW.search(line):
                with_outstanding.append(v)
            else:
                without.append(v)
        if with_outstanding:
            return min(with_outstanding)
        if without:
            return min(without)
        return 0

    return (
        _scan(_WARR_KW, exclude_others=re.compile(r"\b(stock[\s-]?options?|options?\s+d['’]?achat)\b", re.I)),
        _scan(_OPT_KW, exclude_others=re.compile(r"\b(warrants?|bons\s+de\s+souscription)\b", re.I)),
    )


def _all_pages_text(pdf_path: Path) -> str:
    """Return concatenated text of every page (for scanning entire document)."""
    out = []
    try:
        r = pypdf.PdfReader(str(pdf_path))
        for i in range(len(r.pages)):
            try:
                out.append(r.pages[i].extract_text() or "")
            except Exception:
                out.append("")
        return "\n\n".join(out)
    except Exception:
        return ""


# Patterns for "X.Y million common shares issued and outstanding" style
# (ARIS, AAUC use millions-with-decimal). Captured number gets multiplied
# by 1,000,000 at extraction time.
_DIRECT_OUTSTANDING_MILLIONS = [
    re.compile(r"(\d+(?:\.\d+)?)\s+million\s+(?:\w+\s+){0,3}common\s+shares?\s+(?:were\s+|are\s+)?(?:issued\s+and\s+)?outstanding", re.I),
    re.compile(r"common\s+shares?\s+(?:issued\s+and\s+)?outstanding[\s:.]+(\d+(?:\.\d+)?)\s+million", re.I),
]


def _extract_cap_table(pdf_path: Path, notes: list[str]) -> dict:
    """
    Find cap-table fields in an MD&A or AIF.

    Junior issuers put the share-capital summary at the END of the MD&A (a
    dedicated "Outstanding Share Information" section), so the original
    extractor scanned only the last ~40 pages. Senior issuers (Centerra,
    Aris Mining, Allied Gold) put the share count in the INTRODUCTORY pages
    instead. This version scans the full document with direct patterns and
    only falls back to line-based on the last ~40 pages (where false-positive
    risk from the broader scan is low).
    """
    out = {
        "shares_issued_outstanding": None,
        "shares_fully_diluted": None,
        "share_instruments": [],
    }
    full_doc = _all_pages_text(pdf_path)
    if not full_doc:
        notes.append(f"could not read pdf: {pdf_path.name}")
        return out

    last_pages = _last_pages(pdf_path, n=40)
    last_text = "\n\n".join(t for _, t in last_pages)

    # 1. Direct patterns — scan the FULL document. The patterns require
    # specific anchor language ("issued and outstanding") so the false-positive
    # risk on first/middle pages is low.
    for p in _DIRECT_OUTSTANDING:
        m = p.search(full_doc)
        if m:
            v = _to_int(m.group(1))
            if v and 1_000_000 <= v <= 10_000_000_000:
                out["shares_issued_outstanding"] = v
                break

    # 1b. Millions-with-decimal patterns (ARIS, AAUC).
    if out["shares_issued_outstanding"] is None:
        for p in _DIRECT_OUTSTANDING_MILLIONS:
            m = p.search(full_doc)
            if m:
                try:
                    v = int(float(m.group(1)) * 1_000_000)
                    if 1_000_000 <= v <= 10_000_000_000:
                        out["shares_issued_outstanding"] = v
                        break
                except (TypeError, ValueError):
                    pass

    # 2. Line-based fallback uses last-40-pages only (where bilingual juniors
    # like AMX put their cap table — and where the prose-prone risk of
    # picking up issuance-event lines is contained).
    if out["shares_issued_outstanding"] is None:
        out["shares_issued_outstanding"] = _line_match_outstanding(last_text)

    # Reuse `full` variable name for the rest of the function — point it at
    # the last-pages text so warrant/option/instrument extraction stays focused
    # on the cap-table summary section (where instruments live in juniors).
    full = last_text

    if out["shares_issued_outstanding"] is None:
        notes.append("could not locate issued-and-outstanding share count")

    # 3. Fully diluted: try labelled extraction, else compute from outstanding + instruments
    out["shares_fully_diluted"] = _extract_share_count(full, _FULLY_DILUTED)
    warrants_total, options_total = _extract_instrument_counts(full)

    if out["shares_fully_diluted"] is None and out["shares_issued_outstanding"] is not None:
        if warrants_total or options_total:
            out["shares_fully_diluted"] = out["shares_issued_outstanding"] + warrants_total + options_total
            notes.append(
                f"computed fully_diluted = outstanding + {warrants_total} warrants + {options_total} options"
            )

    # 4. share_instruments: detailed (strike+expiry) when present, else count-only stubs
    detailed = _extract_share_instruments(full, notes)
    if detailed:
        out["share_instruments"] = detailed
    else:
        if warrants_total:
            out["share_instruments"].append({
                "type": "warrant", "count": warrants_total,
                "strike_price": None, "expiry": None,
                "raw": "summary count only — strike/expiry not extracted from MD&A summary table",
            })
        if options_total:
            out["share_instruments"].append({
                "type": "option", "count": options_total,
                "strike_price": None, "expiry": None,
                "raw": "summary count only — strike/expiry not extracted from MD&A summary table",
            })

    # 5. Flow-through tranches — detected separately because they live in
    # subsequent-events / financing notes rather than the share-capital
    # summary table that warrants/options sit in.
    ft_tranches = _extract_flow_through_tranches(full, notes)
    out["share_instruments"].extend(ft_tranches)

    return out


def _extract_flow_through_tranches(text: str, notes: list[str]) -> list[dict]:
    """
    Find FT placements mentioned in the MD&A. Returns list of dicts shaped for
    the agent's share_instruments array. Strict: requires both a count and an
    issue price on the same line/sentence to be confident enough to emit.
    Hold-release date is computed as closing-date + 4 months when a closing
    date can be found in the same paragraph; null otherwise.
    """
    out = []
    for m in _FT_LINE.finditer(text):
        count = _to_int(m.group(1))
        try:
            issue_price = float(m.group(2))
        except Exception:
            issue_price = None
        if not count or count < 10_000 or count > 1_000_000_000:
            continue
        if not issue_price or issue_price <= 0 or issue_price > 1000:
            continue

        # Look ~400 chars around the match for a closing-date reference
        seg = text[max(0, m.start() - 400): m.end() + 400]
        cd_match = _FT_CLOSING_DATE.search(seg)
        hold_release = None
        closing_iso = None
        if cd_match:
            closing_iso = _normalize_date(cd_match.group(1))
            if closing_iso:
                try:
                    y, mo, d = (int(p) for p in closing_iso.split("-"))
                    hold_release = _add_months((y, mo, d), 4)
                except Exception:
                    hold_release = None

        out.append({
            "type": "flow_through",
            "count": count,
            "strike_price": None,
            "expiry": None,
            "issue_price": issue_price,
            "hold_release_date": hold_release,
            "notes": (
                f"FT placement"
                + (f" closed {closing_iso}" if closing_iso else "")
                + f" at ${issue_price:.4f}"
            )[:120],
            "raw": text[max(0, m.start() - 60): m.end() + 60].strip()[:200],
        })

    if not out:
        notes.append("no flow-through tranches detected")
    return out


# Match warrant/option line items with counts, strikes, expiries.
# Conservative — we'd rather miss than hallucinate.
_INSTR_LINE = re.compile(
    r"(?P<count>\d{1,3}(?:,\d{3}){1,}|\d{4,})\s+"
    r"(?P<type>warrants?|options?|RSUs?)"
    r"[^\n]*?(?:exercisable\s+at|at\s+\$|at\s+a\s+price\s+of)\s*"
    r"\$?(?P<strike>\d+(?:\.\d+)?)"
    r"[^\n]*?(?:expir(?:e|ing|y)|until|through)\s+"
    r"(?P<expiry>(?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4}|\d{4}[-/]\d{2}[-/]\d{2})",
    re.I,
)


def _extract_share_instruments(text: str, notes: list[str]) -> list[dict]:
    out = []
    for m in _INSTR_LINE.finditer(text):
        kind = m.group("type").lower().rstrip("s")
        kind = "warrant" if kind.startswith("warr") else ("option" if kind.startswith("opt") else "option")
        count = _to_int(m.group("count"))
        try:
            strike = float(m.group("strike"))
        except Exception:
            strike = None
        expiry = _normalize_date(m.group("expiry"))
        if not count:
            continue
        out.append({
            "type": kind,
            "count": count,
            "strike_price": strike,
            "expiry": expiry,
            "raw": m.group(0)[:200],
        })
    if not out:
        notes.append("no warrant/option lines matched the strict pattern")
    return out


_MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}


# Flow-through placement detection.
# Common phrasings in Canadian junior MD&As / press-release recaps:
#   "1,500,000 flow-through shares at $0.50 per share"
#   "FT shares at a price of $0.65"
#   "closed a flow-through private placement of 2,000,000 common shares at $0.40"
# Hold release is typically 4 months from the closing date — when only the
# closing date is given, we add 4 months for hold_release_date.
_FT_LINE = re.compile(
    r"(\d{1,3}(?:[ ,]\d{3}){1,}|\d{4,})\s+"
    r"(?:[\w-]+\s+){0,3}"
    r"(?:flow[\s-]?through|FT)\s+(?:common\s+)?shares?"
    r"[^\n]{0,80}?"
    r"(?:at|@|of)\s*"
    r"\$?(\d+(?:\.\d{1,4})?)",
    re.I,
)
_FT_CLOSING_DATE = re.compile(
    r"(?:closed|closing|completed)\s+(?:on\s+)?"
    r"((?:January|February|March|April|May|June|July|August|September|October|November|December|"
    r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4})",
    re.I,
)


def _add_months(d: tuple[int, int, int], months: int) -> str | None:
    """d is (y, m, d). Return ISO date for d + months. None if input invalid."""
    y, m, day = d
    new_m = m + months
    new_y = y + (new_m - 1) // 12
    new_m = ((new_m - 1) % 12) + 1
    # Clamp day to last day of month if needed
    import calendar
    last = calendar.monthrange(new_y, new_m)[1]
    return f"{new_y:04d}-{new_m:02d}-{min(day, last):02d}"


def _normalize_date(s: str) -> str | None:
    s = s.strip().rstrip(".,")
    m = re.match(r"(\w+)\.?\s+(\d{1,2}),?\s+(\d{4})", s)
    if m:
        mon = _MONTH_MAP.get(m.group(1).lower())
        if mon:
            return f"{m.group(3)}-{mon:02d}-{int(m.group(2)):02d}"
    m = re.match(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return None


# ---------- resource extraction ----------

# Resource summary tables tend to be near front. Search for the "Mineral Resource
# Estimate" header and capture surrounding text. We DO NOT try to parse the
# table — we extract a verbatim chunk and let the agent (or a human reader)
# interpret. Per the prompt: "strings copied verbatim".

_RESOURCE_HEADERS = re.compile(
    r"(?:Mineral\s+Resource\s+(?:Estimate|Statement)"
    r"|Resource\s+Estimate"
    r"|Mineral\s+Resources)",
    re.I,
)
_RESERVE_HEADERS = re.compile(
    r"(?:Mineral\s+Reserve\s+(?:Estimate|Statement)|Mineral\s+Reserves)",
    re.I,
)


def _extract_resource_block(pages: list[tuple[int, str]],
                            header_re: re.Pattern) -> str | None:
    """Return a verbatim ~1500-char block following the first matching header."""
    for idx, t in pages:
        m = header_re.search(t)
        if not m:
            continue
        start = m.start()
        chunk = t[start: start + 2000]
        return chunk.strip()
    return None


def _extract_field_from_block(block: str, category: str) -> str | None:
    """
    Pull the line(s) tagged with the category (Measured/Indicated/Inferred/Proven/Probable).
    Conservative — return raw line text or null.
    """
    if not block:
        return None
    pat = re.compile(rf"^[^\n]*\b{re.escape(category)}\b[^\n]*$", re.I | re.M)
    matches = pat.findall(block)
    if not matches:
        return None
    # Prefer lines with numbers in them (the actual data row, not the heading)
    with_num = [m.strip() for m in matches if re.search(r"\d", m)]
    return with_num[0][:300] if with_num else matches[0].strip()[:300]


# Category patterns. The abbreviated forms (Meas/Ind/Inf) cover compact
# table rows like AMX's; the full forms cover prose ("indicated resource of ...").
_RES_CATEGORIES = {
    "resource_measured": re.compile(r"(?:^|\s)(meas(?:ured)?)\b", re.I),
    "resource_indicated": re.compile(r"(?:^|\s)(ind(?:icated)?)\b(?!.*ndicat)", re.I),
    "resource_inferred":  re.compile(r"(?:^|\s)(inf(?:erred)?)\b", re.I),
    "reserve_proven":     re.compile(r"(?:^|\s)(pro(?:ven)?|prouv[ée]e?)\b", re.I),
    "reserve_probable":   re.compile(r"(?:^|\s)(prob(?:able)?)\b", re.I),
}

# A line that's a real resource-table row has at least 3 numbers (tonnes, grade, contained).
_TABLE_ROW_NUMS = re.compile(r"\d{1,3}(?:[ ,.]?\d{3})*(?:\.\d+)?")


def _extract_resources(latest_43101_path: Path | None,
                       notes: list[str]) -> dict:
    out = {
        "resource_measured": None,
        "resource_indicated": None,
        "resource_inferred": None,
        "reserve_proven": None,
        "reserve_probable": None,
    }
    if not latest_43101_path or not latest_43101_path.exists():
        notes.append("no 43-101 in cache")
        return out

    # Resource summaries are usually in the first 60 pages (executive summary)
    # of a 43-101. Scan those pages line by line.
    try:
        r = pypdf.PdfReader(str(latest_43101_path))
        n_pages = min(60, len(r.pages))
    except Exception:
        notes.append(f"could not read 43-101: {latest_43101_path.name}")
        return out

    # Collect lines from those pages
    lines: list[str] = []
    for i in range(n_pages):
        try:
            t = r.pages[i].extract_text() or ""
            lines.extend(t.split("\n"))
        except Exception:
            continue

    # Skip lines that look like TOC entries, figure captions, or other
    # non-data prose. CG's MD&A had this slip through:
    #   "Table 14-38: Kemess East Indicated and Inferred Mineral Resource
    #    sensitivity; base case NSR cut-off CA$54.10/t ....... 14-61"
    # The original count(".") > 8 missed it (only 7 dots in the leader).
    _TOC_LEADER = re.compile(r"\.{4,}")               # any run of 4+ dots
    _TOC_PREFIX = re.compile(r"^\s*(?:table|figure|schedule|appendix|note)\s+\d", re.I)
    _PAGE_REF = re.compile(r"\b\d+[-–]\d+\s*$|\.\s*\d{1,3}\s*$")  # page ref at end

    def is_data_row(line: str) -> bool:
        if line.count(".") > 8:                       # heavy dot-leader
            return False
        if _TOC_LEADER.search(line):                  # any dot-leader run
            return False
        if _TOC_PREFIX.search(line):                  # "Table N", "Figure N"
            return False
        if _PAGE_REF.search(line):                    # "... 14-61" or "... 287"
            return False
        if len(line.strip()) < 12:
            return False
        nums = _TABLE_ROW_NUMS.findall(line)
        return len(nums) >= 3                          # tonnes + grade + contained ~3+

    for cat, pat in _RES_CATEGORIES.items():
        if out[cat]:
            continue
        for line in lines:
            if not pat.search(line):
                continue
            if not is_data_row(line):
                continue
            # Take the line verbatim, trimmed
            out[cat] = line.strip()[:300]
            break

    if not any(out.values()):
        notes.append("no resource/reserve table rows matched in first 60 pages")
    return out


# ---------- main per-ticker pipeline ----------

def extract_ticker(ticker: str) -> dict:
    notes: list[str] = []
    cache_dir = CACHE_ROOT / ticker.upper()
    manifest_path = cache_dir / "manifest.json"
    if not manifest_path.exists():
        return {
            "ticker": ticker.upper(),
            "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sources": {},
            "shares_issued_outstanding": None,
            "shares_fully_diluted": None,
            "share_instruments": [],
            "resource_measured": None,
            "resource_indicated": None,
            "resource_inferred": None,
            "reserve_proven": None,
            "reserve_probable": None,
            "extraction_notes": ["no manifest.json"],
        }

    manifest = json.loads(manifest_path.read_text())
    by_bucket: dict[str, list] = {}
    for f in manifest.get("filings", []):
        by_bucket.setdefault(f["bucket"], []).append(f)

    # Pick most-recent MD&A for cap-table (annual + interim in one pool),
    # falling back to AIF only if no MD&A at all. Prior version always
    # preferred annual over interim, which made interim-fresh tickers
    # (AWCM, BCM, BZ) look stale.
    cap_source = None
    mda_items = (by_bucket.get("mda") or []) + (by_bucket.get("mda_interim") or [])
    if mda_items:
        cap_source = max(mda_items, key=lambda x: x["date"])
    elif by_bucket.get("aif"):
        cap_source = max(by_bucket["aif"], key=lambda x: x["date"])

    # All 43-101s, latest first
    techs = sorted(by_bucket.get("tech_43101", []), key=lambda x: x["date"], reverse=True)

    cap_data = {
        "shares_issued_outstanding": None,
        "shares_fully_diluted": None,
        "share_instruments": [],
    }
    sources: dict = {}
    if cap_source:
        cap_pdf = cache_dir / cap_source["local_path"]
        if cap_pdf.exists():
            cap_data = _extract_cap_table(cap_pdf, notes)
            sources["cap_table_source"] = {
                "bucket": cap_source["bucket"],
                "date": cap_source["date"],
                "local_path": cap_source["local_path"],
                "sha256": cap_source.get("sha256"),
            }
    else:
        notes.append("no MD&A or AIF in cache")

    res_data = {
        "resource_measured": None, "resource_indicated": None, "resource_inferred": None,
        "reserve_proven": None, "reserve_probable": None,
    }
    if techs:
        latest_43101 = cache_dir / techs[0]["local_path"]
        res_data = _extract_resources(latest_43101, notes)
        sources["tech_43101_source"] = {
            "date": techs[0]["date"],
            "local_path": techs[0]["local_path"],
            "sha256": techs[0].get("sha256"),
        }
    else:
        notes.append("no 43-101 in cache")

    # Also record the financials_annual and AIF source filings so downstream
    # consumers (e.g. the droplet's sync-to-checklist mgmt cmd) can confirm
    # their existence without parsing them. The harvester downloads these
    # PDFs even though extract.py doesn't pull structured fields from them
    # (yet — financials FT extraction is a follow-up).
    for bucket_name, src_key in (
        ("financials_annual", "financials_annual_source"),
        ("aif", "aif_source"),
    ):
        items = by_bucket.get(bucket_name) or []
        if not items:
            continue
        latest = max(items, key=lambda x: x["date"])
        sources[src_key] = {
            "bucket": bucket_name,
            "date": latest["date"],
            "local_path": latest["local_path"],
            "sha256": latest.get("sha256"),
        }

    return {
        "ticker": ticker.upper(),
        "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": sources,
        **cap_data,
        **res_data,
        "extraction_notes": notes,
    }


def write_extracted(ticker: str, data: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / f"{ticker.upper()}.json"
    p.write_text(json.dumps(data, indent=2))
    return p


def all_tickers() -> list[str]:
    return [d.name for d in CACHE_ROOT.iterdir() if d.is_dir()]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python extract.py <TICKER> | --all")
        sys.exit(1)
    if sys.argv[1] == "--all":
        targets = all_tickers()
    else:
        targets = [sys.argv[1]]
    for t in targets:
        d = extract_ticker(t)
        p = write_extracted(t, d)
        print(f"{t}: shares_outstanding={d['shares_issued_outstanding']!r}  "
              f"diluted={d['shares_fully_diluted']!r}  "
              f"instruments={len(d['share_instruments'])}  "
              f"resource_indicated={'Y' if d['resource_indicated'] else '-'}  "
              f"-> {p}")
        if d["extraction_notes"]:
            for n in d["extraction_notes"]:
                print(f"  ! {n}")
