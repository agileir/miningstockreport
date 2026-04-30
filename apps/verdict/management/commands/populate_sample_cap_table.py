"""
Populate sample cap-table data on a single scorecard so the
Cap Table & Overhang Analysis section renders for demonstration.

Idempotent on (scorecard, type, strike_price, expiry) — re-running
without --reset will not create duplicates.

Usage:
    python manage.py populate_sample_cap_table --slug <company-slug>
    python manage.py populate_sample_cap_table --slug <company-slug> --reset

The sample structure is sized for a development-stage junior with a
sub-$1 share price. After running, edit values in /admin/ to match
the actual company — this is purely a demo seed.
"""
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from apps.verdict.models import (
    Company, ShareInstrument, ShareInstrumentType, VerdictScorecard,
)


# Tranche structure for a typical junior gold explorer/developer.
# Strikes are deliberately spread above and below a $0.60 reference
# scoring price so the sensitivity table at 0.5x–3x shows real variation.
SAMPLE_TRANCHES = [
    # (type, count, strike, months_from_scoring_to_expiry, notes)
    (ShareInstrumentType.WARRANT, 28_000_000, Decimal("0.50"),  8,  "Apr-2025 financing tranche"),
    (ShareInstrumentType.WARRANT, 22_000_000, Decimal("0.75"), 14,  "Sep-2024 broker warrants"),
    (ShareInstrumentType.WARRANT, 15_000_000, Decimal("1.20"), 22,  "Strategic placement"),
    (ShareInstrumentType.OPTION,  10_000_000, Decimal("0.40"), 28,  "Director options"),
    (ShareInstrumentType.OPTION,   6_000_000, Decimal("0.85"), 40,  "Management options"),
]

SAMPLE_BASIC_SHARES        = 245_000_000
SAMPLE_FULLY_DILUTED_HINT  = 326_000_000  # Approx basic + all tranches; user can adjust
SAMPLE_FALLBACK_PRICE      = Decimal("0.60")


class Command(BaseCommand):
    help = "Populate sample cap-table data on one scorecard for demo purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--slug", required=True,
            help="Company slug (e.g. 'snowline-gold-corp'). Latest published scorecard is targeted.",
        )
        parser.add_argument(
            "--reset", action="store_true",
            help="Delete existing ShareInstrument tranches on this scorecard before seeding.",
        )

    def handle(self, *args, **options):
        slug = options["slug"]

        try:
            company = Company.objects.get(slug=slug)
        except Company.DoesNotExist:
            raise CommandError(f"No Company with slug '{slug}'.")

        sc = (
            VerdictScorecard.objects
            .filter(company=company, is_published=True)
            .order_by("-scored_at")
            .first()
        )
        if not sc:
            raise CommandError(f"No published scorecard for {company.ticker}.")

        # Backfill basic + fully diluted if missing
        updates = []
        if not sc.shares_issued_outstanding:
            sc.shares_issued_outstanding = SAMPLE_BASIC_SHARES
            updates.append("shares_issued_outstanding")
        if not sc.shares_fully_diluted:
            sc.shares_fully_diluted = SAMPLE_FULLY_DILUTED_HINT
            updates.append("shares_fully_diluted")
        if not sc.current_price:
            sc.current_price = SAMPLE_FALLBACK_PRICE
            updates.append("current_price")
        if updates:
            sc.save(update_fields=updates)
            self.stdout.write(self.style.SUCCESS(f"Set {', '.join(updates)} on scorecard."))

        if options["reset"]:
            n = sc.share_instruments.count()
            sc.share_instruments.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {n} existing tranches."))

        scoring_date = sc.scored_at.date()
        created = skipped = 0
        for kind, count, strike, months, notes in SAMPLE_TRANCHES:
            expiry = scoring_date + timedelta(days=int(months * 30.5))
            obj, was_created = ShareInstrument.objects.get_or_create(
                scorecard=sc,
                type=kind,
                strike_price=strike,
                expiry=expiry,
                defaults={"count": count, "notes": notes},
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Populated {company.ticker} scorecard ({scoring_date.isoformat()}): "
            f"{created} tranches created, {skipped} already present."
        ))
        self.stdout.write(self.style.SUCCESS(f"View: {sc.get_absolute_url()}"))
