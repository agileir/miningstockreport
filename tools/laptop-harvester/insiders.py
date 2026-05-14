"""
Canadian Insider scraper for the laptop-side harvester.

Loads the CI overview page for each ticker, waits for AJAX-injected
insider-filing data to render, parses the rendered DOM, writes structured
JSON to ~/miningstockreport/research_queue/insiders/<TICKER>.json.

Same architecture as sedar_source.py: real Chromium via Playwright +
xvfb + light stealth + persistent profile. Zero LLM cost — pure
DOM parsing.

Output JSON shape:
{
  "ticker": "AMX",
  "fetched_at": "2026-05-06T04:30:00+00:00",
  "source_url": "https://www.canadianinsider.com/company?ticker=AMX",
  "transactions": [
    {
      "insider_name": "Doe, Jane",
      "role": "CEO",
      "transaction_date": "2026-04-15",
      "type": "buy" | "sell" | "grant" | "exercise" | "other",
      "count": 10000,
      "price": 1.23,
      "value_cad": 12300.00,
      "raw": "<verbatim row text for fallback>"
    }
  ],
  "extraction_notes": ["..."]
}
"""
import asyncio
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
PROFILE_DIR = ROOT / "playwright-profile"
OUT_DIR = Path.home() / "miningstockreport" / "research_queue" / "insiders"

CI_URL_TPL = "https://www.canadianinsider.com/company?ticker={ticker}"


# ---------- pacing ----------

async def _hpause(lo=0.5, hi=1.2):
    await asyncio.sleep(random.uniform(lo, hi))


# ---------- browser bootstrap ----------

async def _open_context(p):
    PROFILE_DIR.mkdir(exist_ok=True)
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        viewport={"width": 1440, "height": 900},
        locale="en-CA",
        timezone_id="America/Toronto",
        user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
        args=["--disable-blink-features=AutomationControlled"],
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-CA', 'en']});
    """)
    return ctx, page


# ---------- transaction-type classification ----------

# CI uses different language for the type column. We classify into
# {buy, sell, grant, exercise, other} based on keyword matching.
_TYPE_PATTERNS = [
    (re.compile(r"acquired in the public market|public market.{0,30}buy", re.I), "buy"),
    (re.compile(r"redemption.{0,15}retraction.{0,30}of.{0,15}securities", re.I), "other"),
    (re.compile(r"\b(?:bought|purchase|acquired|acquisition)\b", re.I), "buy"),
    (re.compile(r"\b(?:sold|sale|disposition|disposed)\b", re.I), "sell"),
    (re.compile(r"option.{0,15}exercise|exercise.{0,15}option", re.I), "exercise"),
    (re.compile(r"\b(?:grant(?:ed)?|award(?:ed)?)\b", re.I), "grant"),
]


def _classify_type(txt: str) -> str:
    for pat, kind in _TYPE_PATTERNS:
        if pat.search(txt):
            return kind
    return "other"


# ---------- date / number parsers ----------

_DATE_RE = re.compile(
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4})",
    re.I,
)
_MONTH_MAP = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
              "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}


def _norm_date(s: str) -> str | None:
    m = _DATE_RE.search(s or "")
    if not m:
        return None
    parts = re.match(r"(\w+)\.?\s+(\d{1,2}),?\s+(\d{4})", m.group(1))
    if not parts:
        return None
    mon = _MONTH_MAP.get(parts.group(1)[:3].lower())
    if not mon:
        return None
    return f"{parts.group(3)}-{mon:02d}-{int(parts.group(2)):02d}"


def _parse_int(s: str) -> int | None:
    if not s:
        return None
    digits = re.sub(r"[^\d-]", "", s)
    try:
        return int(digits)
    except Exception:
        return None


def _parse_float(s: str) -> float | None:
    if not s:
        return None
    cleaned = re.sub(r"[^\d.\-]", "", s)
    try:
        return float(cleaned)
    except Exception:
        return None


# ---------- per-ticker scrape ----------

async def fetch_ticker(page, ticker: str) -> dict:
    notes: list[str] = []
    out = {
        "ticker": ticker.upper(),
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_url": CI_URL_TPL.format(ticker=ticker.upper()),
        "transactions": [],
        "extraction_notes": notes,
    }

    await page.goto(out["source_url"], wait_until="domcontentloaded")

    # The "Latest 10 SEDI filings" container starts with a "Loading..." spinner;
    # wait until that placeholder is replaced with real content. Heuristic: wait
    # for any date-pattern text under the heading's container.
    try:
        await page.wait_for_function(
            """() => {
                const heads = Array.from(document.querySelectorAll('div, h1, h2, h3, h4, h5'));
                const target = heads.find(el => /Latest \\d+ SEDI filings/i.test(el.textContent || ''));
                if (!target) return false;
                const container = target.closest('div') || target;
                return /(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\.?\\s+\\d{1,2},?\\s+\\d{4}/i
                       .test(container.textContent || '');
            }""",
            timeout=15000,
        )
    except Exception:
        notes.append("timed out waiting for filings to render (likely no recent insider activity)")
        return out

    # Pull the rendered filings region's structured data.
    rows = await page.evaluate("""() => {
        const heading = Array.from(document.querySelectorAll('div, h1, h2, h3, h4, h5'))
            .find(el => /Latest \\d+ SEDI filings/i.test(el.textContent || ''));
        if (!heading) return [];
        const container = heading.closest('div').parentElement;
        // Look for table rows or div-based row entries with date pattern
        const out = [];
        // Strategy: find all <tr> within container that have at least 4 cells
        container.querySelectorAll('tr').forEach(tr => {
            const cells = Array.from(tr.querySelectorAll('td, th')).map(c => c.textContent.trim());
            if (cells.length >= 4) out.push({type: 'tr', cells});
        });
        // Fallback: look for div rows
        if (out.length === 0) {
            container.querySelectorAll('[class*="row"], [class*="filing"]').forEach(el => {
                const txt = el.textContent.trim();
                if (/(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\.?\\s+\\d{1,2},?\\s+\\d{4}/i.test(txt)
                    && txt.length < 800) {
                    out.push({type: 'div', html: el.outerHTML.slice(0, 1000), text: txt.slice(0, 400)});
                }
            });
        }
        return out;
    }""")

    if not rows:
        notes.append("no filing rows extracted from rendered DOM")
        return out

    # Parse rows — both <tr>-based (cells array) and <div>-based (text fallback)
    for r in rows:
        if r.get("type") == "tr":
            cells = r["cells"]
            # Common CI column ordering: filer / role / date / shares / price / value / type
            # Be flexible; find by content patterns
            full = " | ".join(cells)
            tx_date = _norm_date(full)
            if not tx_date:
                continue
            # Extract candidates by position (best-effort)
            insider_name = cells[0] if cells else ""
            role = cells[1] if len(cells) > 1 else ""
            type_text = cells[-1] if cells else ""
            # Find the cell that looks like a count (largest int on the row)
            counts = [c for c in (_parse_int(x) for x in cells) if c is not None]
            count = max(counts, default=None)
            # Find a price-like cell (small positive float)
            prices = [c for c in (_parse_float(x) for x in cells) if c is not None and 0 < c < 10000]
            # Filter prices that aren't share counts
            non_count_prices = [p for p in prices if p != count and (count is None or p < count / 100)]
            price = non_count_prices[0] if non_count_prices else None

            out["transactions"].append({
                "insider_name": insider_name[:200],
                "role": role[:100],
                "transaction_date": tx_date,
                "type": _classify_type(type_text or full),
                "count": count,
                "price": price,
                "value_cad": (count * price) if (count and price) else None,
                "raw": full[:500],
            })
        else:
            txt = r.get("text", "")
            tx_date = _norm_date(txt)
            if not tx_date:
                continue
            counts = re.findall(r"\d{1,3}(?:,\d{3})+|\d{4,}", txt)
            counts_int = [int(c.replace(",", "")) for c in counts]
            count = max(counts_int, default=None)
            out["transactions"].append({
                "insider_name": "",
                "role": "",
                "transaction_date": tx_date,
                "type": _classify_type(txt),
                "count": count,
                "price": None,
                "value_cad": None,
                "raw": txt[:500],
            })

    if not out["transactions"]:
        notes.append("rows found but none yielded a parseable transaction")
    return out


def write_output(ticker: str, data: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / f"{ticker.upper()}.json"
    p.write_text(json.dumps(data, indent=2))
    return p


async def run(tickers: list[str]):
    async with async_playwright() as p:
        ctx, page = await _open_context(p)
        try:
            for t in tickers:
                print(f"  [{t}] fetching...", flush=True)
                try:
                    data = await fetch_ticker(page, t)
                    path = write_output(t, data)
                    print(f"  [{t}] wrote {len(data['transactions'])} transactions -> {path}")
                    if data["extraction_notes"]:
                        for n in data["extraction_notes"]:
                            print(f"     ! {n}")
                except Exception as e:
                    print(f"  [{t}] FAILED: {e}")
                await _hpause(2.0, 4.0)
        finally:
            await ctx.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python insiders.py <TICKER> [TICKER ...]")
        sys.exit(1)
    asyncio.run(run(sys.argv[1:]))
