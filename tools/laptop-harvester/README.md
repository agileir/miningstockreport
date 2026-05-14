# Laptop Harvester Backup

Snapshot of the laptop-side SEDAR+ harvester and PDF extractor that lives on `chaugen@192.168.1.79:~/sedar-harvester/`. Backed up to the repo so the code survives a laptop disk failure.

**This is a backup, not the live source.** Edits made here do not flow back to the laptop. To deploy a change, edit on the laptop, then re-run the backup step.

## Files

- `sedar_source.py` — Playwright SEDAR+ harvester. Public: `harvest_sedar_latest(profile, ticker)`. Uses persistent Chromium context + xvfb + stealth init to defeat Reblaze.
- `extract.py` — rule-based PDF extractor (pypdf + regex). Reads `~/sedar-cache/<TICKER>/*.pdf`, writes `research_queue/extracted/<TICKER>.json`. Handles cap-table, share instruments, resource/reserve rows, flow-through tranches.
- `filings.py` — `Filing` dataclass and `latest_by_bucket()` helper used by `sedar_source.py`.
- `auth.py`, `fetch.py` — StockWatch fallback (rarely used since SEDAR+ direct started working).
- `run_nightly.sh` — cron wrapper. Pulls repo, reads `research_queue/companies.json`, runs harvester + extractor per ticker, commits extracted JSON, pushes.
- `insiders.py` — Canadian Insider scraper (WIP, parser does not work yet — paused 2026-05-13).
- `inspect_ci_rendered.py` — Playwright DOM inspector for CI page debugging.

## Running on the laptop

```
ssh chaugen@192.168.1.79
cd ~/sedar-harvester
source venv/bin/activate
xvfb-run -a --server-args='-screen 0 1440x900x24' python sedar_source.py 'Profile Name Inc.' TICKER
python extract.py TICKER
```

## Cron

`30 6 * * * $HOME/sedar-harvester/run_nightly.sh >> $HOME/sedar-harvester/cron.log 2>&1`

Runs at 06:30 UTC daily, after the droplet's 05:50 UTC `export_queues.sh` has written `companies.json`.
