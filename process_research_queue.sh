#!/bin/bash
# Process pending scorecard files pushed by the verdict research agent.
# Cron: */30 * * * * /home/deploy/miningstock/process_research_queue.sh >> /var/log/miningstock/research_queue.log 2>&1
set -e

cd /home/deploy/miningstock
git pull origin main --quiet 2>/dev/null

QUEUE_DIR="research_queue"
source venv/bin/activate

for f in "$QUEUE_DIR"/scorecard_*.json; do
    [ -f "$f" ] || continue
    echo "$(date '+%Y-%m-%d %H:%M:%S') Processing $f"
    python manage.py shell --settings=config.settings.production -c "
import json, sys
from datetime import timezone as tz
from django.utils import timezone
from apps.verdict.models import Company, VerdictScorecard, VerdictChoice

data = json.load(open('$f'))
ticker = data['ticker']
company = Company.objects.get(ticker__iexact=ticker)
confidence = data.get('confidence', 'low').lower()

scorecard = VerdictScorecard.objects.create(
    company=company,
    management_score=int(data['management_score']),
    management_notes=data.get('management_notes', ''),
    geology_score=int(data['geology_score']),
    geology_notes=data.get('geology_notes', ''),
    capital_score=int(data['capital_score']),
    capital_notes=data.get('capital_notes', ''),
    catalyst_score=int(data['catalyst_score']),
    catalyst_notes=data.get('catalyst_notes', ''),
    acquisition_score=int(data['acquisition_score']),
    acquisition_notes=data.get('acquisition_notes', ''),
    verdict=data['verdict'].upper(),
    analyst_summary=data.get('analyst_summary', ''),
    nav_per_share=data.get('nav_per_share'),
    current_price=data.get('current_price'),
    is_published=(confidence == 'high'),
    scored_at=timezone.now(),
)
company.needs_research = False
company.save(update_fields=['needs_research'])
print(f'{ticker}: {scorecard.verdict} ({scorecard.composite_score}/25) published={scorecard.is_published}')
"
    rm "$f"
    git add "$QUEUE_DIR/"
    git commit -m "Processed research queue: $(basename $f)" --quiet
    git push origin main --quiet
    echo "$(date '+%Y-%m-%d %H:%M:%S') Done processing $f"
done
