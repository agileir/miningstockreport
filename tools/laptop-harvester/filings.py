
"""
StockWatch SEDAR filing-list scraper.
"""
import re
import sys
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from auth import get_session, BASE, authed_get

SEARCH_URL = BASE + "/News/Sedar"


@dataclass
class Filing:
    ticker: str
    date: str
    type_code: str
    bucket: Optional[str]
    lang: str
    doc_url: str
    doc_id: str
    synopsis: str


def classify(type_code: str) -> tuple[Optional[str], str]:
    t = type_code.upper()
    norm = re.sub(r"[^A-Z0-9]", "", t)

    lang = "unknown"
    if re.search(r"\bENGLISH\b|_EN\b|\(E\)", t) or norm.endswith("EN"):
        lang = "en"
    elif re.search(r"\bFRENCH\b|_FR\b|\(F\)", t) or norm.endswith("FR"):
        lang = "fr"

    bucket: Optional[str] = None
    if "TECHNICALREPORT" in norm and "43101" in norm:
        bucket = "tech_43101"
    elif "INTERIMMDA" in norm or ("INTERIM" in norm and "MDA" in norm):
        bucket = "mda_interim"
    elif norm.startswith("MDA") or "ANNUALMDA" in norm:
        if "INTERIM" not in norm:
            bucket = "mda"
    elif "ANNUALINFORMATIONFORM" in norm or norm.startswith("AIF"):
        bucket = "aif"
    elif "AUDITEDANNUALFINANCIALSTATEMENTS" in norm:
        bucket = "financials_annual"

    return bucket, lang


def list_filings(ticker: str, date_from: str = "20200101", date_to: str = "20260501") -> list[Filing]:
    session = get_session()
    url = f"{SEARCH_URL}?C:{ticker}"

    r = authed_get(session, url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    def v(name: str) -> str:
        el = soup.find("input", {"name": name})
        return el.get("value", "") if el else ""

    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": v("__VIEWSTATE"),
        "__VIEWSTATEGENERATOR": v("__VIEWSTATEGENERATOR"),
        "ctl00$MainContent$tPublicFrom": date_from,
        "ctl00$MainContent$tPublicTo": date_to,
        "ctl00$MainContent$tPublicSymbol": ticker,
        "ctl00$MainContent$dPublicDoctype": "",
        "ctl00$MainContent$bPublic.x": "1",
        "ctl00$MainContent$bPublic.y": "1",
    }

    r2 = session.post(url, data=data, timeout=30)
    r2.raise_for_status()
    soup2 = BeautifulSoup(r2.text, "html.parser")

    target = None
    for t in soup2.find_all("table"):
        rows = t.find_all("tr")
        if not rows:
            continue
        head = rows[0].get_text(" | ", strip=True)
        if "Issuer" in head and "Date" in head and "Type" in head:
            target = t
            break
    if target is None:
        return []

    out: list[Filing] = []
    for row in target.find_all("tr")[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) < 5:
            continue

        # Find PDF link anywhere in the row
        link = row.find("a", href=re.compile(r"Sedardoc/\d+\.pdf"))
        if not link:
            continue
        href = link["href"]
        doc_url = urljoin(BASE, href)
        m = re.search(r"Sedardoc/(\d+)\.pdf", href)
        doc_id = m.group(1) if m else ""

        date = cells[3].get_text(strip=True)
        # Type cell may contain "<code> | <industry>"
        type_cell = cells[4].get_text("|", strip=True)
        type_code = type_cell.split("|")[0].strip()

        # Synopsis: any cell after position 4 that has substantive text other than the link
        synopsis = ""
        for c in cells[5:]:
            txt = c.get_text(" ", strip=True)
            if txt and txt.lower() != "document":
                synopsis = txt[:300]
                break

        bucket, lang = classify(type_code)
        out.append(Filing(
            ticker=ticker, date=date, type_code=type_code,
            bucket=bucket, lang=lang,
            doc_url=doc_url, doc_id=doc_id, synopsis=synopsis,
        ))
    return out


def latest_by_bucket(filings: list[Filing], lang_pref: str = "en") -> dict[str, Filing]:
    by_bucket: dict[str, list[Filing]] = {}
    for f in filings:
        if f.bucket:
            by_bucket.setdefault(f.bucket, []).append(f)
    chosen: dict[str, Filing] = {}
    for bucket, items in by_bucket.items():
        preferred = [i for i in items if i.lang == lang_pref]
        pool = preferred if preferred else items
        chosen[bucket] = max(pool, key=lambda x: x.date)
    return chosen


if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AMX"
    fs = list_filings(ticker)
    print(f"{ticker}: {len(fs)} filings parsed")
    by_bucket: dict[str, int] = {}
    for f in fs:
        k = f.bucket or "OTHER"
        by_bucket[k] = by_bucket.get(k, 0) + 1
    for k, n in sorted(by_bucket.items(), key=lambda x: -x[1]):
        print(f"  {k:20s}  {n}")
    print()
    print("=== latest per bucket (en preferred) ===")
    for bucket, f in sorted(latest_by_bucket(fs).items()):
        print(f"  {bucket:20s}  {f.date}  {f.lang}  {f.type_code[:55]:55s}  {f.doc_url}")
