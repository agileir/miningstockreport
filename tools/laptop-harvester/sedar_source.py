"""
SEDAR+ source for the harvester.

Drives the SEDAR+ "Search and download documents" page with real
Chromium + persistent profile + light stealth + human pacing.

Returns filings.Filing objects (compatible with the existing
StockWatch pipeline) and writes PDFs into ~/sedar-cache/<TICKER>/
matching the layout fetch.py expects.

Public API:
    harvest_sedar_latest(profile, ticker=None) -> dict[bucket, manifest_entry]

NOTE: Selectors marked SPECULATIVE are educated guesses from the user's
screenshot walkthrough; verify and adjust after first live run.
"""
import asyncio
import hashlib
import json
import random
import re
import sys
import unicodedata
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


def _strip_accents(s: str) -> str:
    """
    Remove accents from a string. SEDAR+ profile lookup returns no matches
    when the typed text contains accents that don't appear in the underlying
    profile name (verified by user 2026-05-05). E.g. "Entrée" must be typed
    as "Entree" to match. Apply this to the typed-name path; profile-number
    overrides bypass this entirely.
    """
    if not s:
        return s
    return "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )

from playwright.async_api import async_playwright, Page, Locator

from filings import Filing, latest_by_bucket

ROOT = Path(__file__).resolve().parent
PROFILE_DIR = ROOT / "playwright-profile"
PROFILE_NUMBER_CACHE = ROOT / "profile_cache.json"
# Operator-curated CSV pulled nightly via the repo: ticker,profile_number,...
# Takes precedence over the auto-populated profile_cache.json. Lets us bypass
# autocomplete fuzzy-matching for tickers where the profile name registered
# on SEDAR+ doesn't match the operations name field (e.g. issuer-rename
# suffixes like "(formerly Core Nickel Corp.)").
CURATED_OVERRIDES_CSV = Path.home() / "miningstockreport" / "research_queue" / "tickers_profiles.csv"
CACHE_ROOT = Path.home() / "sedar-cache"

LANDING_URL = "https://www.sedarplus.ca/landingpage/?_locale=en"
SEARCH_URL = (
    "https://www.sedarplus.ca/csa-party/service/create.html"
    "?targetAppCode=csa-party&service=searchDocuments&_locale=en"
)

# SEDAR+ doc-type dropdown label per internal bucket.
# Verified labels (2026-05-02) by dumping the live Select2 option list.
DOCTYPE_FOR_BUCKET = {
    "tech_43101":        "Technical report (NI 43-101)",
    "mda":               "Annual MD&A",
    "mda_interim":       "Interim MD&A",
    "financials_annual": "Audited annual financial statements",
    "aif":               "Annual information form",
}

DEFAULT_DATE_FROM = "01/01/2020"  # DD/MM/YYYY


# ----------------- profile-number cache -----------------

def _load_cache() -> dict:
    return json.loads(PROFILE_NUMBER_CACHE.read_text()) if PROFILE_NUMBER_CACHE.exists() else {}


def _load_curated_overrides() -> dict[str, str]:
    """ticker (uppercase) -> profile_number from operator-curated CSV."""
    out: dict[str, str] = {}
    if not CURATED_OVERRIDES_CSV.exists():
        return out
    import csv
    try:
        with CURATED_OVERRIDES_CSV.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                t = (row.get("ticker") or "").strip().upper()
                n = (row.get("profile_number") or "").strip()
                if t and n:
                    out[t] = n
    except Exception:
        pass
    return out

def _save_cache(d: dict) -> None:
    PROFILE_NUMBER_CACHE.write_text(json.dumps(d, indent=2, sort_keys=True))


# ----------------- human pacing -----------------

async def _hpause(lo=0.8, hi=2.4):
    await asyncio.sleep(random.uniform(lo, hi))

async def _htype(loc: Locator, text: str):
    await loc.click()
    await _hpause(0.2, 0.6)
    for ch in text:
        await loc.type(ch, delay=random.uniform(60, 180))
        if random.random() < 0.05:
            await asyncio.sleep(random.uniform(0.3, 0.9))


# ----------------- browser bootstrap -----------------

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
            "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ),
        accept_downloads=True,
        args=["--disable-blink-features=AutomationControlled"],
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-CA', 'en']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
    """)
    return ctx, page


async def _warm_up(page: Page):
    if "sedarplus.ca" not in page.url:
        await page.goto(LANDING_URL, wait_until="domcontentloaded")
        await _hpause(3, 6)
    await page.goto(SEARCH_URL, wait_until="domcontentloaded")
    await _hpause(2, 4)


# ----------------- form interaction (SPECULATIVE selectors) -----------------

async def _fill_profile(page: Page, profile: str, ticker: str | None = None) -> None:
    cache = _load_cache()
    overrides = _load_curated_overrides()
    field = page.get_by_placeholder("Profile name or number")
    await field.click()
    await _hpause(0.2, 0.5)
    # Clear via keyboard (so autocomplete sees the input event flow). Without
    # this, persistent-profile session sometimes preserves prior form text and
    # subsequent typing appends, breaking the autocomplete match.
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Delete")
    await _hpause(0.2, 0.4)

    # Precedence:
    # 1. Operator-curated CSV by ticker (deterministic; bypasses fuzzy matching)
    # 2. Auto-populated profile_cache.json by name (built up from prior runs)
    # 3. The name itself (autocomplete will resolve), accent-stripped
    override_num = overrides.get((ticker or "").upper()) if ticker else None
    cached_num = cache.get(profile)
    typed = override_num or cached_num or _strip_accents(profile)
    # Always type (don't .fill) so jQuery-UI autocomplete keypress handlers fire.
    await _htype(field, typed)
    await _hpause(0.9, 1.6)

    # jQuery-UI autocomplete dropdown
    menu = page.locator("ul.ui-autocomplete:visible")
    await menu.first.wait_for(state="visible", timeout=10000)

    # Prefer an option whose text contains the typed string (case-insensitive
    # AND accent-folded — SEDAR+ dropdown text may include accents that the
    # typed text doesn't, or vice versa).
    items = menu.locator("li")
    count = await items.count()
    chosen = None
    typed_l = _strip_accents(typed).lower()
    for i in range(count):
        txt = _strip_accents(await items.nth(i).inner_text()).lower()
        if typed_l in txt:
            chosen = items.nth(i)
            break
    if chosen is None:
        if count == 1:
            # Autocomplete narrowed to one — trust it (e.g. issuer renamed).
            chosen = items.first
        else:
            print(f"     WARN: no autocomplete option contains {typed!r}; "
                  f"using first of {count} candidates")
            chosen = items.first

    label = await chosen.inner_text()
    m = re.search(r"\((\d{5,})\)", label)
    if m and not cached_num:
        cache[profile] = m.group(1)
        _save_cache(cache)
    await chosen.click()
    await _hpause(1.0, 2.0)


async def _select_doctype(page: Page, label: str) -> None:
    # Document type is a Select2 multi-select (id="DocumentType"). The visible
    # widget exposes a search textarea with aria-labelledby="DocumentType_label".
    # Clear any prior selection first, then open + type-to-filter + click option.
    await page.evaluate("""() => {
        if (window.jQuery && jQuery('#DocumentType').length) {
            jQuery('#DocumentType').val(null).trigger('change');
        }
    }""")
    await _hpause(0.3, 0.7)

    search = page.locator("textarea[aria-labelledby='DocumentType_label']")
    await search.click()
    await _hpause(0.4, 0.9)
    # Type a discriminating fragment so Select2 narrows the option list.
    typed = label[:20]
    await search.type(typed, delay=random.randint(70, 150))
    await _hpause(0.7, 1.3)

    # EXACT text match — substring matching picked sibling labels like
    # "Amended & restated technical report (NI 43-101)" before the one we want.
    opts = page.locator(".select2-results__option")
    await opts.first.wait_for(state="visible", timeout=8000)
    n = await opts.count()
    for i in range(n):
        if (await opts.nth(i).inner_text()).strip() == label:
            await opts.nth(i).click()
            await _hpause(0.6, 1.2)
            return
    available = [(await opts.nth(i).inner_text()).strip() for i in range(n)]
    raise RuntimeError(f"No exact match for doctype {label!r}. Available: {available}")


async def _set_dates(page: Page, date_from: str, date_to: str) -> None:
    # Inputs are jQuery-UI datepickers with stable IDs. fill() dispatches
    # input+change; we follow with Tab to fire blur (datepicker's validation
    # hook runs on blur).
    if date_from:
        await page.locator("#SubmissionDate").fill(date_from)
        await page.locator("#SubmissionDate").press("Tab")
        await _hpause(0.2, 0.4)
    if date_to:
        await page.locator("#SubmissionDate2").fill(date_to)
        await page.locator("#SubmissionDate2").press("Tab")
        await _hpause(0.2, 0.4)


async def _click_search(page: Page) -> None:
    # Snapshot banner text BEFORE click so we can detect a state transition.
    # Without this, the previous bucket's banner ("Displaying 1-N of M") was
    # still in the DOM and our wait returned true immediately.
    prev_banner = await page.evaluate(
        "() => { const b = document.querySelector('.appPagerBanner'); return b ? b.textContent.trim() : ''; }"
    )

    await page.get_by_role("button", name=re.compile(r"^\s*Search\s*$")).first.click()

    try:
        await page.wait_for_function(
            """(prev) => {
                const b = document.querySelector('.appPagerBanner');
                const txt = b ? b.textContent.trim() : '';
                // New banner present AND different from previous
                if (txt && txt !== prev && /Displaying|No\\s+results/i.test(txt)) return true;
                // Or explicit no-match message in the body
                return /no\\s+search\\s+results\\s+that\\s+match/i.test(document.body.innerText);
            }""",
            arg=prev_banner,
            timeout=30000,
        )
    except Exception:
        pass
    await _hpause(1.5, 3.0)


def _norm_date(s: str) -> str:
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    m = re.search(r"(\d{1,2})\s+(\w{3})\s+(\d{4})", s)
    if not m:
        return s.strip()
    d, mon, y = m.groups()
    return f"{y}{months.get(mon, 0):02d}{int(d):02d}"


async def _parse_results(page: Page, ticker: str, bucket: str) -> list[Filing]:
    """
    Parse SEDAR+ search results. Results are in div.appSearchResults; each row
    contains a download link to viewInstance/resource.html with a drmKey.
    drmKey is session-scoped, so we don't rely on it for cross-run dedup.
    """
    links = page.locator(".appSearchResults a[href*='resource.html'][href*='drmKey=']")
    n = await links.count()
    out: list[Filing] = []
    for i in range(n):
        link = links.nth(i)
        href = await link.evaluate("a => a.href")  # always absolute
        text = (await link.inner_text()).strip()
        if not text:
            continue
        # Walk up to a row container that includes the date string.
        row_text = await link.evaluate("""(a) => {
            let el = a;
            for (let i = 0; i < 8 && el.parentElement; i++) {
                el = el.parentElement;
                if (/\\d{1,2}\\s+[A-Z][a-z]{2}\\s+\\d{4}/.test(el.textContent)) break;
            }
            return el.textContent;
        }""")
        date = _norm_date(row_text)
        m = re.search(r"drmKey=([a-f0-9]+)", href)
        doc_id = m.group(1) if m else hashlib.sha1(href.encode()).hexdigest()[:12]
        lang = "fr" if "french" in text.lower() else "en"
        out.append(Filing(
            ticker=ticker, date=date, type_code=text,
            bucket=bucket, lang=lang,
            doc_url=href, doc_id=doc_id, synopsis="",
        ))
    return out


async def _download_via_click(page: Page, link_locator: Locator, dest: Path) -> int:
    async with page.expect_download(timeout=60000) as info:
        await link_locator.click()
    d = await info.value
    await d.save_as(str(dest))
    return dest.stat().st_size


# ----------------- single-session orchestrator -----------------

async def _harvest_async(profile: str, ticker: str,
                         buckets: list[str],
                         date_from: str, date_to: str) -> dict[str, list[dict]]:
    """
    For tech_43101: download every English filing (multi-property reports).
    For other buckets: download the latest English filing only.
    Dedup is by (bucket, date, type_code) since drmKey is session-scoped.
    """
    out_dir = CACHE_ROOT / ticker
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() \
               else {"ticker": ticker, "filings": []}
    seen = {(e["bucket"], e["date"], e.get("type_code", "")) for e in manifest["filings"]}

    out: dict[str, list[dict]] = {}

    async with async_playwright() as p:
        ctx, page = await _open_context(p)
        try:
            await _warm_up(page)
            await _fill_profile(page, profile, ticker=ticker)

            for bucket in buckets:
                print(f"  [{ticker}] {bucket:20s} searching...", flush=True)
                await _select_doctype(page, DOCTYPE_FOR_BUCKET[bucket])
                await _set_dates(page, date_from, date_to)
                await _click_search(page)

                filings = await _parse_results(page, ticker, bucket)
                en = [f for f in filings if f.lang == "en"] or filings
                if not en:
                    print(f"     no filings")
                    await _hpause(2.0, 5.0)
                    continue

                if bucket == "tech_43101":
                    chosen = sorted(en, key=lambda f: f.date)
                else:
                    chosen = [max(en, key=lambda f: f.date)]

                out[bucket] = []
                for f in chosen:
                    key = (f.bucket, f.date, f.type_code)
                    local_name = f"{f.bucket}-{f.date}.pdf"
                    if bucket == "tech_43101":
                        # extra safety against rare same-date 43-101s on
                        # different projects
                        local_name = f"{f.bucket}-{f.date}-{f.doc_id[:8]}.pdf"
                    local_path = out_dir / local_name

                    if key in seen and local_path.exists() and local_path.stat().st_size > 0:
                        print(f"     already cached: {local_name}")
                        for e in manifest["filings"]:
                            if (e["bucket"], e["date"], e.get("type_code", "")) == key:
                                out[bucket].append(e)
                                break
                        continue

                    link = page.locator(f"a[href*='{f.doc_id}']").first
                    try:
                        size = await _download_via_click(page, link, local_path)
                        data = local_path.read_bytes()
                        entry = {
                            **asdict(f),
                            "local_path": local_name,
                            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            "size_bytes": size,
                            "sha256": hashlib.sha256(data).hexdigest(),
                        }
                        manifest["filings"] = [
                            e for e in manifest["filings"]
                            if (e["bucket"], e["date"], e.get("type_code", "")) != key
                        ]
                        manifest["filings"].append(entry)
                        manifest_path.write_text(json.dumps(manifest, indent=2))
                        out[bucket].append(entry)
                        print(f"     OK {f.date} {size//1024} KB")
                    except Exception as e:
                        print(f"     download FAILED ({f.date}): {e}")
                    await _hpause(1.5, 3.5)

                await _hpause(2.5, 6.0)
        finally:
            await ctx.close()
    return out


# ----------------- public sync entrypoint -----------------

def harvest_sedar_latest(profile: str, ticker: str | None = None,
                         buckets: list[str] | None = None,
                         date_from: str = DEFAULT_DATE_FROM,
                         date_to: str | None = None) -> dict[str, list[dict]]:
    ticker = (ticker or profile).upper().strip()
    buckets = buckets or list(DOCTYPE_FOR_BUCKET.keys())
    if date_to is None:
        date_to = datetime.now().strftime("%d/%m/%Y")
    return asyncio.run(_harvest_async(profile, ticker, buckets, date_from, date_to))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python sedar_source.py <profile-name> [TICKER] [BUCKETS]")
        print("  BUCKETS: comma-separated subset of "
              + ",".join(DOCTYPE_FOR_BUCKET.keys()))
        sys.exit(1)
    profile = sys.argv[1]
    ticker = sys.argv[2] if len(sys.argv) > 2 else None
    buckets = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    print(f"SEDAR+ harvest: profile={profile!r} ticker={ticker!r} buckets={buckets}")
    result = harvest_sedar_latest(profile, ticker, buckets=buckets)
    total = sum(len(v) for v in result.values())
    print(f"\n{total} filings across {len(result)} buckets")
    for bucket, entries in result.items():
        for e in entries:
            print(f"  {bucket:20s} {e['local_path']}  ({e['size_bytes']//1024} KB)")
