"""
Management command to fetch gold and copper spot prices from Yahoo Finance.

Usage:
    python manage.py sync_commodities

Cron (hourly):
    0 * * * * cd /home/deploy/miningstock && /home/deploy/miningstock/venv/bin/python manage.py sync_commodities --settings=config.settings.production
"""
from django.core.management.base import BaseCommand
import yfinance as yf
from apps.core.models import CommodityPrice


COMMODITIES = [
    {"symbol": "GC=F", "name": "Gold", "unit": "/oz"},
    {"symbol": "HG=F", "name": "Copper", "unit": "/lb"},
]


class Command(BaseCommand):
    help = "Fetch latest gold and copper prices from Yahoo Finance"

    def handle(self, *args, **options):
        symbols = [c["symbol"] for c in COMMODITIES]
        tickers = yf.Tickers(" ".join(symbols))

        for commodity in COMMODITIES:
            sym = commodity["symbol"]
            try:
                ticker = tickers.tickers[sym]
                info = ticker.fast_info
                price = info.last_price
                prev_close = info.previous_close

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
