#!/bin/bash
# Process company data files pushed by the company-data agent.
# Cron: */30 * * * * /home/deploy/miningstock/process_company_data.sh >> /var/log/miningstock/company_data.log 2>&1
set -e

cd /home/deploy/miningstock
git pull origin main --quiet 2>/dev/null

QUEUE_DIR="research_queue"
DEADLETTER_DIR="$QUEUE_DIR/.failed"
mkdir -p "$DEADLETTER_DIR"
source venv/bin/activate

for f in "$QUEUE_DIR"/company_*.json; do
    [ -f "$f" ] || continue
    echo "$(date '+%Y-%m-%d %H:%M:%S') Processing $f"
    if python manage.py shell --settings=config.settings.production -c "
import json, sys, traceback
from apps.verdict.models import Company, Exchange

try:
    data = json.load(open('$f'))
    ticker = data['ticker']
    exchange_raw = (data.get('exchange') or '').upper()
    # Prefer (ticker, exchange) scoped lookup to handle duplicate tickers across exchanges.
    qs = Company.objects.filter(ticker__iexact=ticker)
    if exchange_raw in Exchange.values:
        scoped = qs.filter(exchange=exchange_raw)
        if scoped.exists():
            qs = scoped
    n = qs.count()
    if n == 0:
        print(f'Company {ticker} not found, skipping')
        sys.exit(0)
    if n > 1:
        ids = list(qs.values_list('id', flat=True))
        print(f'AMBIGUOUS: {n} companies match ticker={ticker} exchange={exchange_raw} (ids={ids}); skipping — resolve duplicate before retrying')
        sys.exit(1)
    company = qs.first()

    if company.data_filled:
        print(f'{ticker} already filled, skipping')
        sys.exit(0)

    exchange = exchange_raw if exchange_raw in Exchange.values else 'OTHER'
    company.name              = data.get('name', company.name) or company.ticker
    company.exchange          = exchange
    company.description       = (data.get('description') or '')
    company.website           = (data.get('website') or '')
    company.jurisdiction      = (data.get('jurisdiction') or '')
    company.primary_commodity = (data.get('primary_commodity') or '')
    company.data_filled       = True
    company.save()
    print(f'{ticker}: filled — {company.name} ({company.exchange}, {company.primary_commodity})')
except SystemExit:
    raise
except Exception as e:
    traceback.print_exc()
    print(f'ERROR processing $f: {e}')
    sys.exit(1)
"; then
        rm "$f"
        git add "$QUEUE_DIR/"
        git commit -m "Processed company data: $(basename $f)" --quiet
        git push origin main --quiet
        echo "$(date '+%Y-%m-%d %H:%M:%S') Done processing $f"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') FAILED processing $f — moving to $DEADLETTER_DIR"
        mv "$f" "$DEADLETTER_DIR/"
    fi
done
