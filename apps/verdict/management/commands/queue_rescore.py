"""
Flag the next batch of companies for re-scoring.
Picks companies that have existing scorecards but haven't been
re-scored with the updated NAV discount model.

Usage:
    python manage.py queue_rescore --batch 5

Cron (nightly, before the export):
    40 5 * * * cd /home/deploy/miningstock && source venv/bin/activate && python manage.py queue_rescore --batch 5 --settings=config.settings.production
"""
from django.core.management.base import BaseCommand
from apps.verdict.models import Company


class Command(BaseCommand):
    help = "Flag next batch of companies with old scorecards for re-research"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch", type=int, default=5,
            help="Number of companies to flag per run (default: 5)",
        )

    def handle(self, *args, **options):
        batch_size = options["batch"]

        # Find companies that have scorecards, haven't been flagged,
        # and haven't been re-scored yet (scored before the model update on 2026-04-14)
        from django.utils import timezone
        from datetime import datetime
        cutoff = timezone.make_aware(datetime(2026, 4, 15))

        candidates = (
            Company.objects.filter(
                scorecards__isnull=False,
                needs_research=False,
            )
            .exclude(scorecards__scored_at__gte=cutoff)
            .distinct()
            .order_by("ticker")[:batch_size]
        )

        if not candidates:
            self.stdout.write("All companies have been re-scored. Nothing to queue.")
            return

        tickers = []
        for company in candidates:
            company.needs_research = True
            company.save(update_fields=["needs_research"])
            tickers.append(company.ticker)

        self.stdout.write(self.style.SUCCESS(
            f"Flagged {len(tickers)} companies for re-scoring: {', '.join(tickers)}"
        ))
