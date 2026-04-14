#!/bin/bash
# Process pending scorecard files pushed by the verdict research agent.
# Cron: */30 * * * * /home/deploy/miningstock/process_research_queue.sh >> /var/log/miningstock/research_queue.log 2>&1
set -e

cd /home/deploy/miningstock
git pull origin main --quiet 2>/dev/null

QUEUE_DIR="research_queue"
source venv/bin/activate

# Clear the companies.json queue file after scorecards are processed
PROCESSED=0

for f in "$QUEUE_DIR"/scorecard_*.json; do
    [ -f "$f" ] || continue
    echo "$(date '+%Y-%m-%d %H:%M:%S') Processing $f"
    python manage.py shell --settings=config.settings.production -c "
import json, requests
from decimal import Decimal
from django.utils import timezone
from apps.verdict.models import Company, VerdictScorecard, VerdictChoice

data = json.load(open('$f'))
ticker = data['ticker']
company = Company.objects.get(ticker__iexact=ticker)
confidence = data.get('confidence', 'low').lower()

# Fetch current stock price from Yahoo Finance
current_price = data.get('current_price')
if not current_price:
    # Build Yahoo Finance symbol from ticker + exchange
    exchange = company.exchange
    yf_suffix = {
        'TSXV': '.V', 'TSX': '.TO', 'ASX': '.AX',
        'LSE': '.L', 'NYSE': '', 'OTC': '',
    }
    suffix = yf_suffix.get(exchange, '')
    yf_symbol = ticker.replace('.V', '').replace('.TO', '').replace('.AX', '') + suffix
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{yf_symbol}?range=1d&interval=1d'
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        resp.raise_for_status()
        meta = resp.json()['chart']['result'][0]['meta']
        current_price = round(meta['regularMarketPrice'], 4)
        print(f'  Fetched price for {yf_symbol}: \${current_price}')
    except Exception as e:
        print(f'  Could not fetch price for {yf_symbol}: {e}')

# Delete all old scorecards for this company before creating the new one
old_count = VerdictScorecard.objects.filter(company=company).count()
if old_count > 0:
    VerdictScorecard.objects.filter(company=company).delete()
    print(f'  Deleted {old_count} old scorecard(s) for {ticker}')

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
    current_price=current_price,
    is_published=(confidence == 'high'),
    scored_at=timezone.now(),
)
company.needs_research = False
company.save(update_fields=['needs_research'])
print(f'{ticker}: {scorecard.verdict} ({scorecard.composite_score}/25) published={scorecard.is_published} price=\${current_price or \"N/A\"}')
"
    rm "$f"
    git add "$QUEUE_DIR/"
    git commit -m "Processed research queue: $(basename $f)" --quiet
    git push origin main --quiet
    PROCESSED=1
    echo "$(date '+%Y-%m-%d %H:%M:%S') Done processing $f"
done

# Remove companies.json so the agent doesn't re-research the same companies
if [ "$PROCESSED" -gt 0 ] && [ -f "$QUEUE_DIR/companies.json" ]; then
    rm "$QUEUE_DIR/companies.json"
    git add "$QUEUE_DIR/"
    git commit -m "Clear research queue after processing" --quiet
    git push origin main --quiet
    echo "$(date '+%Y-%m-%d %H:%M:%S') Cleared companies.json"
fi
