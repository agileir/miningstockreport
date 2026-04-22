"""
Promote CompanyQueue entries to Company records at a controlled pace.

Picks the N oldest ACTIVE entries without a linked Company, creates a
Company record for each with data_filled=False, needs_research=False, links
the FK back to the queue entry, and flips the queue status to PROMOTED.

The subsequent pipeline (export_unfilled_companies → data-fill agent →
queue_rescore → export_research_queue → research agent) handles the rest.

Cron (intended to run before export_queues.sh):
    40 5 * * * cd /home/deploy/miningstock && venv/bin/python manage.py promote_queue --batch 3 --settings=config.settings.production

Usage:
    python manage.py promote_queue --batch 3
"""
from django.core.management.base import BaseCommand

from apps.verdict.models import Company, CompanyQueue, CompanyQueueStatus


class Command(BaseCommand):
    help = "Promote N active queue entries to Company records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch", type=int, default=3,
            help="Max number of queue entries to promote per run (default: 3)",
        )

    def handle(self, *args, **options):
        batch = options["batch"]
        candidates = (
            CompanyQueue.objects.filter(
                status=CompanyQueueStatus.ACTIVE,
                company__isnull=True,
            )
            .order_by("created_at", "ticker")[:batch]
        )

        if not candidates:
            self.stdout.write("No active queue entries to promote.")
            return

        promoted = 0
        linked   = 0
        for entry in candidates:
            existing = Company.objects.filter(
                ticker=entry.ticker, exchange=entry.exchange,
            ).first()
            if existing:
                entry.company = existing
                entry.status = CompanyQueueStatus.PROMOTED
                entry.save(update_fields=["company", "status"])
                linked += 1
                self.stdout.write(f"Linked {entry.exchange}:{entry.ticker} to existing Company")
                continue

            company = Company.objects.create(
                ticker=entry.ticker,
                exchange=entry.exchange,
                name=entry.name,
                primary_commodity=entry.primary_commodity,
                jurisdiction=entry.country,
                needs_research=False,
                data_filled=False,
            )
            entry.company = company
            entry.status = CompanyQueueStatus.PROMOTED
            entry.save(update_fields=["company", "status"])
            promoted += 1
            self.stdout.write(f"Promoted {entry.exchange}:{entry.ticker} ({entry.name})")

        self.stdout.write(self.style.SUCCESS(
            f"Done: promoted {promoted} new, linked {linked} existing."
        ))
