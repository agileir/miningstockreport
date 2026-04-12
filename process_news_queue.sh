#!/bin/bash
# Process pending news files pushed by the remote Claude agent.
# Cron: */15 * * * * /home/deploy/miningstock/process_news_queue.sh >> /var/log/miningstock/news_queue.log 2>&1
set -e

cd /home/deploy/miningstock
git pull origin main --quiet 2>/dev/null

QUEUE_DIR="news_queue"

for f in "$QUEUE_DIR"/pending_*.json; do
    [ -f "$f" ] || continue
    echo "$(date '+%Y-%m-%d %H:%M:%S') Processing $f"
    source venv/bin/activate
    python manage.py update_news --source agent --file "$f" --settings=config.settings.production
    rm "$f"
    git add "$QUEUE_DIR/"
    git commit -m "Processed news queue file: $(basename $f)" --quiet
    git push origin main --quiet
    echo "$(date '+%Y-%m-%d %H:%M:%S') Done processing $f"
done
