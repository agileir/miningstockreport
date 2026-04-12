#!/bin/bash
# Process company data files pushed by the company-data agent.
# Cron: */30 * * * * /home/deploy/miningstock/process_company_data.sh >> /var/log/miningstock/company_data.log 2>&1
set -e

cd /home/deploy/miningstock
git pull origin main --quiet 2>/dev/null

QUEUE_DIR="research_queue"
source venv/bin/activate

for f in "$QUEUE_DIR"/company_*.json; do
    [ -f "$f" ] || continue
    echo "$(date '+%Y-%m-%d %H:%M:%S') Processing $f"
    python manage.py shell --settings=config.settings.production -c "
import json
from apps.verdict.models import Company, Exchange

data = json.load(open('$f'))
ticker = data['ticker']
try:
    company = Company.objects.get(ticker__iexact=ticker)
except Company.DoesNotExist:
    print(f'Company {ticker} not found, skipping')
    exit()

if company.data_filled:
    print(f'{ticker} already filled, skipping')
    exit()

# Map exchange string to Exchange choice
exchange_map = {v.lower(): k for k, v in dict(Exchange.choices).items()}
exchange_raw = data.get('exchange', '').upper()
# Try direct match first, then fuzzy
exchange = exchange_raw if exchange_raw in Exchange.values else 'OTHER'

company.name = data.get('name', company.name) or company.ticker
company.exchange = exchange
company.description = data.get('description', '') or ''
company.website = data.get('website', '') or ''
company.jurisdiction = data.get('jurisdiction', '') or ''
company.primary_commodity = data.get('primary_commodity', '') or ''
company.data_filled = True
company.save()
print(f'{ticker}: filled — {company.name} ({company.exchange}, {company.primary_commodity})')
"
    rm "$f"
    git add "$QUEUE_DIR/"
    git commit -m "Processed company data: $(basename $f)" --quiet
    git push origin main --quiet
    echo "$(date '+%Y-%m-%d %H:%M:%S') Done processing $f"
done
