"""
Re-run sanity validation against every existing ChecklistItem row, without
touching the underlying JSON. Useful when sanity rules change and we want
to refresh notes / pass/fail across the corpus.

Cross-field context (basic / diluted) is built from the company's other
checklist items so ratio checks still work.
"""
from django.core.management.base import BaseCommand

from apps.verdict import sanity
from apps.verdict.models import (
    Company, CompanyHarvestState, HarvestStateChoice,
    ChecklistItem, ChecklistItemCategory,
)


def _ctx_for(company):
    """Return {basic, diluted} pulled from this company's checklist items."""
    rows = {ci.key: ci.value for ci in company.checklist_items.all()}
    return {
        "basic":   rows.get("shares_issued_outstanding"),
        "diluted": rows.get("shares_fully_diluted"),
    }


def _refresh_harvest_state(company):
    state, _ = CompanyHarvestState.objects.get_or_create(company=company)
    required = list(company.checklist_items.filter(category=ChecklistItemCategory.REQUIRED))
    unsatisfied = [item for item in required if not item.is_satisfied]
    state.ready_for_verdict = (len(unsatisfied) == 0)
    state.blockers_summary = "; ".join(
        f"{i.key}({i.get_status_display()})" for i in unsatisfied
    )[:1500]
    state.status = HarvestStateChoice.READY if state.ready_for_verdict else HarvestStateChoice.BLOCKED
    state.save()
    return state


class Command(BaseCommand):
    help = "Re-run sanity validators against all ChecklistItem rows (no JSON read)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--tickers", nargs="*", default=None,
            help="Limit to specific tickers (default: all companies).",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Show what would change without writing.",
        )

    def handle(self, *args, **opts):
        qs = Company.objects.all()
        if opts["tickers"]:
            qs = qs.filter(ticker__in=[t.upper() for t in opts["tickers"]])

        n_companies = 0
        n_items     = 0
        n_changed   = 0
        n_ready     = 0
        n_blocked   = 0

        for company in qs:
            ctx = _ctx_for(company)
            items = list(company.checklist_items.all())
            if not items:
                continue
            n_companies += 1
            for ci in items:
                n_items += 1
                result = sanity.validate(ci.key, ci.value, **ctx)
                new_passed = result.passed
                new_notes  = result.with_prefix()
                if ci.sanity_check_passed != new_passed or ci.sanity_check_notes != new_notes:
                    n_changed += 1
                    if not opts["dry_run"]:
                        ci.sanity_check_passed = new_passed
                        ci.sanity_check_notes = new_notes
                        ci.save(update_fields=["sanity_check_passed", "sanity_check_notes"])
            if not opts["dry_run"]:
                state = _refresh_harvest_state(company)
                if state.ready_for_verdict:
                    n_ready += 1
                else:
                    n_blocked += 1

        prefix = "[DRY RUN] " if opts["dry_run"] else ""
        self.stdout.write(self.style.SUCCESS(
            f"{prefix}Rechecked {n_items} items across {n_companies} companies: "
            f"{n_changed} updated. {n_ready} ready / {n_blocked} blocked."
        ))
