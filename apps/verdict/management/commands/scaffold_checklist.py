"""
Scaffold ChecklistItem + CompanyHarvestState rows for every Company.

Idempotent: only creates rows that don't already exist. Safe to re-run after
adding new keys to REQUIRED_CHECKLIST_KEYS.
"""
from django.core.management.base import BaseCommand

from apps.verdict.models import (
    Company, CompanyHarvestState, ChecklistItem,
    ChecklistItemStatus, REQUIRED_CHECKLIST_KEYS,
)


class Command(BaseCommand):
    help = "Create CompanyHarvestState + ChecklistItem rows for any company missing them."

    def add_arguments(self, parser):
        parser.add_argument(
            "--tickers", nargs="*", default=None,
            help="Limit to specific tickers (default: all companies).",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Show what would be created without writing.",
        )

    def handle(self, *args, **opts):
        qs = Company.objects.all()
        if opts["tickers"]:
            qs = qs.filter(ticker__in=opts["tickers"])

        states_created = 0
        items_created  = 0
        for company in qs:
            # 1. CompanyHarvestState
            if not hasattr(company, "harvest_state"):
                if not opts["dry_run"]:
                    CompanyHarvestState.objects.create(company=company)
                states_created += 1

            # 2. ChecklistItem rows for every key in the catalog
            existing_keys = set(
                company.checklist_items.values_list("key", flat=True)
            )
            for key, category, _desc, _sanity in REQUIRED_CHECKLIST_KEYS:
                if key in existing_keys:
                    continue
                if not opts["dry_run"]:
                    ChecklistItem.objects.create(
                        company=company,
                        key=key,
                        category=category,
                        status=ChecklistItemStatus.PENDING,
                    )
                items_created += 1

        msg = (
            f"Created {states_created} CompanyHarvestState rows, "
            f"{items_created} ChecklistItem rows."
        )
        if opts["dry_run"]:
            msg = "[DRY RUN] " + msg
        self.stdout.write(self.style.SUCCESS(msg))
