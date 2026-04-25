#!/bin/bash
# Export flagged companies for both data-fill and research agents.
# Commits and pushes to GitHub so remote agents can pick them up.
# Cron: 50 5 * * * /home/deploy/miningstock/export_queues.sh >> /var/log/miningstock/export_queues.log 2>&1
set -e

cd /home/deploy/miningstock
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting queue export"

# Pull latest to avoid conflicts
git pull origin main --quiet 2>/dev/null

# Queue next batch of companies for re-scoring + new research.
# TEMPORARY (2026-04-24 to 2026-06-24): bumped from --batch 5 / --new 3 (default)
# to --batch 6 / --new 6 for ~6 scorecards/night through end of June 2026.
# REVERT after 2026-06-24 → restore: --batch 5 (and drop --new).
python manage.py queue_rescore --batch 6 --new 6 --settings=config.settings.production 2>&1

# Export unfilled companies (for company-data-agent)
python manage.py export_unfilled_companies --settings=config.settings.production 2>&1

# Export research-flagged companies (for verdict-research-agent)
python manage.py export_research_queue --settings=config.settings.production 2>&1

# Commit and push if anything changed
git add research_queue/
if ! git diff --cached --quiet; then
    git commit -m "Export queues $(date -u +%Y-%m-%d)" --quiet
    git push origin main --quiet
    echo "$(date '+%Y-%m-%d %H:%M:%S') Pushed queue updates to GitHub"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') No queue changes to push"
fi
