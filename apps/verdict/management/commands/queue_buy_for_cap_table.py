"""
Flag BUY-rated companies missing cap-table data for re-research.

Targets companies whose latest published scorecard is BUY-rated but lacks
`shares_issued_outstanding` (proxy for "no cap-table data was filled in").
Sets `needs_research=True` so the existing research agent picks them up
on the next run. The agent will regenerate the scorecard with cap-table
data per the updated research-agent-schema.md.

Usage:
    python manage.py queue_buy_for_cap_table --dry-run         # preview
    python manage.py queue_buy_for_cap_table                   # flag all
    python manage.py queue_buy_for_cap_table --limit 10        # cap batch

Why BUY-only: cap-table risk most directly affects the strength of a BUY
thesis — an underwritten BUY with hidden warrant overhang is a more
expensive miss than the same gap on a WATCH or AVOID. Once BUY-rated
coverage is filled in, run the same logic for WATCH if desired.
"""
from django.core.management.base import BaseCommand
from django.db.models import OuterRef, Subquery

from apps.verdict.models import Company, CompanyTier, VerdictChoice, VerdictScorecard


class Command(BaseCommand):
    help = "Flag BUY-rated companies missing cap-table data for re-research."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit", type=int, default=None,
            help="Maximum companies to flag this run (default: all matching).",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Print what would be flagged without saving.",
        )
        parser.add_argument(
            "--juniors-only", action="store_true",
            help="Restrict to tier=junior (covers explorers and developers; excludes mid-tier and major producers).",
        )

    def handle(self, *args, **options):
        latest_scorecard = (
            VerdictScorecard.objects
            .filter(company=OuterRef("pk"), is_published=True)
            .order_by("-scored_at")
        )

        candidates = (
            Company.objects
            .annotate(
                _latest_verdict=Subquery(latest_scorecard.values("verdict")[:1]),
                _latest_basic=Subquery(latest_scorecard.values("shares_issued_outstanding")[:1]),
            )
            .filter(
                _latest_verdict=VerdictChoice.BUY,
                _latest_basic__isnull=True,
                needs_research=False,
            )
            .order_by("ticker")
        )

        if options["juniors_only"]:
            candidates = candidates.filter(tier=CompanyTier.JUNIOR)

        if options["limit"]:
            candidates = candidates[: options["limit"]]

        candidates = list(candidates)

        if not candidates:
            self.stdout.write("No BUY-rated companies missing cap-table data — nothing to flag.")
            return

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN — would flag {len(candidates)} companies:"
            ))
            for c in candidates:
                self.stdout.write(f"  {c.exchange}:{c.ticker:8} — {c.name}")
            return

        flagged = 0
        for c in candidates:
            c.needs_research = True
            c.save(update_fields=["needs_research"])
            flagged += 1

        tickers = ", ".join(c.ticker for c in candidates)
        self.stdout.write(self.style.SUCCESS(
            f"Flagged {flagged} BUY-rated companies for re-research: {tickers}"
        ))
        self.stdout.write(
            "Next: the 5:50 AM cron will export companies.json; the agent picks it up on its next run."
        )
