#!/bin/bash
# Process pending scorecard files pushed by the verdict research agent.
# Cron: */30 * * * * /home/deploy/miningstock/process_research_queue.sh >> /var/log/miningstock/research_queue.log 2>&1
set -e

cd /home/deploy/miningstock
git pull origin main --quiet 2>/dev/null

QUEUE_DIR="research_queue"
TOKEN=$(grep NEWS_INGEST_TOKEN .env | cut -d= -f2)

for f in "$QUEUE_DIR"/scorecard_*.json; do
    [ -f "$f" ] || continue
    echo "$(date '+%Y-%m-%d %H:%M:%S') Processing $f"
    curl -s -X POST http://localhost:8000/api/v1/verdicts/ingest/ \
        -H "Content-Type: application/json" \
        -H "X-Ingest-Token: $TOKEN" \
        -d @"$f"
    echo ""
    rm "$f"
    git add "$QUEUE_DIR/"
    git commit -m "Processed research queue: $(basename $f)" --quiet
    git push origin main --quiet
    echo "$(date '+%Y-%m-%d %H:%M:%S') Done processing $f"
done
