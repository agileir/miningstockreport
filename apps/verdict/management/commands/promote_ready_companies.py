"""
Flip `needs_research=True` on companies whose harvest state is READY and
which don't yet have a scorecard in the last N days.

This is the auto-promoter that connects the checklist quality gate to the
existing research-queue flow. After this runs, `export_research_queue`
picks up the flagged companies and writes `companies.json` for the agent.

Cron (runs between sync and export):
    40 5 * * * cd /home/deploy/miningstock && venv/bin/python manage.py promote_ready_companies --settings=config.settings.production
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone as djtz

from apps.verdict.models import (
    Company, CompanyHarvestState, HarvestStateChoice, VerdictScorecard,
)


class Command(BaseCommand):
    help = "Auto-flag READY companies for research (respecting recent-scorecard cooldown)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--cooldown-days", type=int, default=30,
            help="Skip companies with a scorecard newer than this (default 30).",
        )
        parser.add_argument(
            "--cap", type=int, default=5,
            help="Maximum companies to promote in one run (default 5, matches agent queue cap).",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Show what would be flagged without writing.",
        )

    def handle(self, *args, **opts):
        cutoff = djtz.now() - timedelta(days=opts["cooldown_days"])

        # Candidates: harvest state READY, not already flagged for research
        candidates = (
            CompanyHarvestState.objects
            .filter(status=HarvestStateChoice.READY, ready_for_verdict=True)
            .select_related("company")
            .order_by("last_successful_harvest")  # oldest-harvest first → freshest data prioritised
        )

        promoted = []
        skipped_cooldown = []
        skipped_flagged = []

        for state in candidates:
            company = state.company
            if company.needs_research:
                skipped_flagged.append(company.ticker)
                continue
            recent = VerdictScorecard.objects.filter(
                company=company, scored_at__gte=cutoff,
            ).exists()
            if recent:
                skipped_cooldown.append(company.ticker)
                continue
            if len(promoted) >= opts["cap"]:
                break
            promoted.append(company.ticker)
            if not opts["dry_run"]:
                company.needs_research = True
                company.save(update_fields=["needs_research"])

        prefix = "[DRY RUN] " if opts["dry_run"] else ""
        self.stdout.write(self.style.SUCCESS(
            f"{prefix}Promoted {len(promoted)} ready companies: "
            f"{', '.join(promoted) if promoted else '(none)'}"
        ))
        if skipped_flagged:
            self.stdout.write(f"  Already flagged ({len(skipped_flagged)}): {', '.join(skipped_flagged)}")
        if skipped_cooldown:
            self.stdout.write(f"  In cooldown ({len(skipped_cooldown)}): {', '.join(skipped_cooldown)}")
