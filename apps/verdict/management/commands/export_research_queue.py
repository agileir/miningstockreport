"""
Export companies flagged for AI research to research_queue/companies.json.

Usage:
    python manage.py export_research_queue

Cron (runs 10 min before the research agent):
    50 5 * * * cd /home/deploy/miningstock && venv/bin/python manage.py export_research_queue --settings=config.settings.production
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from apps.verdict.models import Company


class Command(BaseCommand):
    help = "Export companies needing research to research_queue/companies.json"

    def handle(self, *args, **options):
        companies = Company.objects.filter(needs_research=True)

        if not companies.exists():
            self.stdout.write("No companies flagged for research.")
            return

        data = [
            {
                "ticker": c.ticker,
                "name": c.name,
                "exchange": c.exchange,
                "website": c.website,
                "primary_commodity": c.primary_commodity,
                "jurisdiction": c.jurisdiction,
            }
            for c in companies
        ]

        queue_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / "research_queue"
        queue_dir.mkdir(exist_ok=True)
        output_path = queue_dir / "companies.json"
        output_path.write_text(json.dumps(data, indent=2))

        self.stdout.write(self.style.SUCCESS(
            f"Exported {len(data)} companies to {output_path}"
        ))
