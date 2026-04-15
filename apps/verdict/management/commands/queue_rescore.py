"""
Flag the next batch of companies for re-scoring or new research.

Phase 1 (rescore): Picks 5 companies with old scorecards (pre NAV-discount model).
Phase 2 (new research): Once rescoring is done, picks 3 companies that have
    never been researched (no scorecards, data_filled=True, not already flagged).

Usage:
    python manage.py queue_rescore --batch 5 --new 3
"""
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.verdict.models import Company


class Command(BaseCommand):
    help = "Flag companies for re-scoring or new research"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch", type=int, default=5,
            help="Number of companies to re-score per run (default: 5)",
        )
        parser.add_argument(
            "--new", type=int, default=3,
            help="Number of new companies to research per run after rescoring is done (default: 3)",
        )

    def handle(self, *args, **options):
        batch_size = options["batch"]
        new_size = options["new"]
        cutoff = timezone.make_aware(datetime(2026, 4, 15))

        # Phase 1: Re-score companies with old scorecards
        rescore_candidates = (
            Company.objects.filter(
                scorecards__isnull=False,
                needs_research=False,
            )
            .exclude(scorecards__scored_at__gte=cutoff)
            .distinct()
            .order_by("ticker")[:batch_size]
        )

        if rescore_candidates:
            tickers = []
            for company in rescore_candidates:
                company.needs_research = True
                company.save(update_fields=["needs_research"])
                tickers.append(company.ticker)
            self.stdout.write(self.style.SUCCESS(
                f"Re-score: flagged {len(tickers)} companies: {', '.join(tickers)}"
            ))
            return

        # Phase 2: All rescoring done — queue new companies that have never been researched
        self.stdout.write("All companies re-scored. Looking for new companies to research...")

        new_candidates = (
            Company.objects.filter(
                data_filled=True,
                needs_research=False,
                scorecards__isnull=True,
            )
            .order_by("ticker")[:new_size]
        )

        if not new_candidates:
            self.stdout.write("No new companies to research. All caught up.")
            return

        tickers = []
        for company in new_candidates:
            company.needs_research = True
            company.save(update_fields=["needs_research"])
            tickers.append(company.ticker)

        self.stdout.write(self.style.SUCCESS(
            f"New research: flagged {len(tickers)} companies: {', '.join(tickers)}"
        ))
