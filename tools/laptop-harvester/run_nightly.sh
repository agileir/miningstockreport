#!/bin/bash
# Nightly SEDAR+ harvest. Pulls research_queue/companies.json from the
# miningstockreport repo and harvests each ticker into ~/sedar-cache/.
# Designed for cron — no interactive input.
#
# Usage:
#   run_nightly.sh             # process all companies
#   run_nightly.sh --limit N   # process only the first N (for testing)

set -u

HERE="$HOME/sedar-harvester"
REPO="$HOME/miningstockreport"
QUEUE="$REPO/research_queue/companies.json"
PER_COMPANY_TIMEOUT=600

LIMIT=0
if [ "${1:-}" = "--limit" ] && [ -n "${2:-}" ]; then
    LIMIT="$2"
fi

cd "$HERE" || exit 1

# Update local repo clone (clone if missing)
if [ -d "$REPO/.git" ]; then
    git -C "$REPO" pull --quiet --ff-only origin main 2>&1 || echo "WARN: git pull failed (continuing with stale checkout)"
else
    git clone --quiet https://github.com/agileir/miningstockreport.git "$REPO" 2>&1 || { echo "FATAL: git clone failed"; exit 1; }
fi

if [ ! -f "$QUEUE" ]; then
    echo "FATAL: $QUEUE not found"
    exit 1
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "=================================================================="
echo "nightly harvest start: $(date -Iseconds)"
echo "queue: $QUEUE  limit: $LIMIT"
echo "=================================================================="

# Emit "ticker|name" lines into a temp file, optionally truncated to LIMIT.
python -c '
import json, sys
for c in json.load(open(sys.argv[1])):
    if c.get("ticker") and c.get("name"):
        print(c["ticker"] + "|" + c["name"])
' "$QUEUE" > /tmp/_nightly_queue.txt
if [ "$LIMIT" -gt 0 ]; then
    head -n "$LIMIT" /tmp/_nightly_queue.txt > /tmp/_nightly_queue.tmp
    mv /tmp/_nightly_queue.tmp /tmp/_nightly_queue.txt
fi

total=$(wc -l < /tmp/_nightly_queue.txt)
echo "$total companies to process"
echo

i=0
fail=0
while IFS='|' read -r ticker name; do
    i=$((i+1))
    echo "------------------------------------------------------------------"
    echo "[$i/$total] $(date -Iseconds)  $ticker  ($name)"
    echo "------------------------------------------------------------------"
    if ! timeout "$PER_COMPANY_TIMEOUT" xvfb-run -a --server-args="-screen 0 1440x900x24" \
            python sedar_source.py "$name" "$ticker" 2>&1; then
        echo ">>> FAILED: $ticker"
        fail=$((fail+1))
    fi
    echo
done < /tmp/_nightly_queue.txt

echo "=================================================================="
echo "nightly harvest end: $(date -Iseconds)"
echo "$fail failures of $total"
echo "=================================================================="

# ----------------------------------------------------------------------
# Extract structured fields from cached PDFs and commit to the repo so
# the hosted research-agent can read them via git pull. This is what
# prevents the agent from trying (and failing) to fetch SEDAR+ itself.
# ----------------------------------------------------------------------
echo
echo "=== extracting structured cap-table + resource fields ==="
python "$HERE/extract.py" --all || echo "WARN: extract.py exited non-zero (continuing)"

cd "$REPO" || exit 0
git add research_queue/extracted/ 2>/dev/null
if git diff --cached --quiet; then
    echo "no extracted-data changes to commit"
else
    git -c user.name="sedar-harvester" -c user.email="harvester@miningstockreport.com" \
        commit -m "Update extracted SEDAR+ data $(date -I)" >/dev/null
    if git push --quiet origin main 2>&1 | grep -v -E '^$'; then
        echo "pushed extracted-data update"
    else
        echo "extracted-data push attempted"
    fi
fi

rm -f /tmp/_nightly_queue.txt
exit 0
