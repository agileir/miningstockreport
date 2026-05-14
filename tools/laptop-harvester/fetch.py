
"""
Fetch + cache SEDAR filings to local disk.

Layout:
  ~/sedar-cache/
    <TICKER>/
      manifest.json
      <bucket>-<date>-<doc_id>.pdf
"""
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from auth import get_session, authed_get
from filings import Filing, list_filings, latest_by_bucket

CACHE_ROOT = Path.home() / "sedar-cache"


def _ticker_dir(ticker: str) -> Path:
    d = CACHE_ROOT / ticker.upper()
    d.mkdir(parents=True, exist_ok=True)
    return d


def _manifest_path(ticker: str) -> Path:
    return _ticker_dir(ticker) / "manifest.json"


def load_manifest(ticker: str) -> dict:
    p = _manifest_path(ticker)
    if not p.exists():
        return {"ticker": ticker.upper(), "filings": []}
    return json.loads(p.read_text())


def save_manifest(ticker: str, m: dict) -> None:
    _manifest_path(ticker).write_text(json.dumps(m, indent=2))


def _filename(f: Filing) -> str:
    return f"{f.bucket}-{f.date}-{f.doc_id}.pdf"


def _already_cached(manifest: dict, doc_id: str, local_path: Path) -> bool:
    for entry in manifest["filings"]:
        if entry["doc_id"] == doc_id and local_path.exists() and local_path.stat().st_size > 0:
            return True
    return False


def fetch_filing(filing: Filing, force: bool = False) -> dict:
    """Download a single filing. Returns the manifest entry. Idempotent."""
    ticker_dir = _ticker_dir(filing.ticker)
    local_name = _filename(filing)
    local_path = ticker_dir / local_name
    manifest = load_manifest(filing.ticker)

    if not force and _already_cached(manifest, filing.doc_id, local_path):
        for e in manifest["filings"]:
            if e["doc_id"] == filing.doc_id:
                return e

    session = get_session()
    r = authed_get(session, filing.doc_url, timeout=60)
    r.raise_for_status()
    if not r.content.startswith(b"%PDF-"):
        raise RuntimeError(
            f"Not a PDF for {filing.doc_id} ({filing.type_code}); "
            f"got {r.headers.get('content-type', '')}, first bytes={r.content[:20]!r}"
        )

    local_path.write_bytes(r.content)
    sha = hashlib.sha256(r.content).hexdigest()
    entry = {
        **asdict(filing),
        "local_path": local_name,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "size_bytes": len(r.content),
        "sha256": sha,
    }
    manifest["filings"] = [e for e in manifest["filings"] if e["doc_id"] != filing.doc_id]
    manifest["filings"].append(entry)
    save_manifest(filing.ticker, manifest)
    return entry


def harvest_latest(ticker: str, buckets: list[str] | None = None) -> dict[str, dict]:
    if buckets is None:
        buckets = ["mda", "aif", "financials_annual", "tech_43101"]

    fs = list_filings(ticker)
    chosen = latest_by_bucket(fs)

    out: dict[str, dict] = {}
    for bucket in buckets:
        if bucket not in chosen:
            print(f"  [{ticker}] {bucket:20s} -- no filing found")
            continue
        f = chosen[bucket]
        print(f"  [{ticker}] {bucket:20s} {f.date}  {f.type_code[:50]:50s}", end=" ", flush=True)
        try:
            entry = fetch_filing(f)
            print(f"OK  {entry['size_bytes']//1024} KB")
            out[bucket] = entry
        except Exception as e:
            print(f"FAIL  {e}")
    return out


if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AMX"
    print(f"Harvesting {ticker} -> {CACHE_ROOT / ticker.upper()}")
    result = harvest_latest(ticker)
    print()
    print(f"Cached {len(result)} filings")
    for bucket, e in result.items():
        sz = e['size_bytes'] // 1024
        lp = e['local_path']
        print(f"  {bucket:20s} {lp}  ({sz} KB)")
