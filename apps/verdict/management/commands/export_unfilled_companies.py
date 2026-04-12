"""
Export companies that need data filled (ticker entered, data_filled=False).

Usage:
    python manage.py export_unfilled_companies

Cron (runs before the company-data agent):
    45 5 * * * cd /home/deploy/miningstock && source venv/bin/activate && python manage.py export_unfilled_companies --settings=config.settings.production
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from apps.verdict.models import Company


class Command(BaseCommand):
    help = "Export companies needing data fill to research_queue/unfilled_companies.json"

    def handle(self, *args, **options):
        companies = Company.objects.filter(data_filled=False)

        if not companies.exists():
            self.stdout.write("No unfilled companies.")
            return

        data = [{"ticker": c.ticker} for c in companies]

        queue_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / "research_queue"
        queue_dir.mkdir(exist_ok=True)
        output_path = queue_dir / "unfilled_companies.json"
        output_path.write_text(json.dumps(data, indent=2))

        self.stdout.write(self.style.SUCCESS(
            f"Exported {len(data)} unfilled companies to {output_path}"
        ))
