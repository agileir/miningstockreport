"""
Management command to fetch gold and copper spot prices from Yahoo Finance.

Usage:
    python manage.py sync_commodities

Cron (hourly):
    0 * * * * cd /home/deploy/miningstock && /home/deploy/miningstock/venv/bin/python manage.py sync_commodities --settings=config.settings.production
"""
import requests
from django.core.management.base import BaseCommand
from apps.core.models import CommodityPrice


COMMODITIES = [
    {"symbol": "GC=F", "name": "Gold", "unit": "/oz"},
    {"symbol": "SI=F", "name": "Silver", "unit": "/oz"},
    {"symbol": "HG=F", "name": "Copper", "unit": "/lb"},
]

YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=2d&interval=1d"
HEADERS = {"User-Agent": "Mozilla/5.0"}


class Command(BaseCommand):
    help = "Fetch latest gold and copper prices from Yahoo Finance"

    def handle(self, *args, **options):
        for commodity in COMMODITIES:
            sym = commodity["symbol"]
            try:
                resp = requests.get(
                    YAHOO_URL.format(symbol=sym),
                    headers=HEADERS,
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                result = data["chart"]["result"][0]
                meta = result["meta"]
                price = meta["regularMarketPrice"]
                prev_close = meta.get("chartPreviousClose") or meta.get("previousClose")

                change_pct = None
                if prev_close and prev_close > 0:
                    change_pct = round(((price - prev_close) / prev_close) * 100, 2)

                CommodityPrice.objects.update_or_create(
                    symbol=sym,
                    defaults={
                        "name": commodity["name"],
                        "price": round(price, 2),
                        "change_pct": change_pct,
                        "unit": commodity["unit"],
                    },
                )
                self.stdout.write(self.style.SUCCESS(
                    f"{commodity['name']}: ${price:.2f} ({change_pct:+.2f}%)"
                ))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to fetch {commodity['name']}: {e}"))
