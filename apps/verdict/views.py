import re
from datetime import date as date_type

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from .commodities import COMMODITIES, get_commodity
from .models import Company, CompanyTier, VerdictScorecard, VerdictChoice


class CompanyListView(ListView):
    model = Company
    template_name = "verdict/company_list.html"
    context_object_name = "companies"
    paginate_by = 20

    def get_queryset(self):
        qs = Company.objects.prefetch_related("scorecards")

        # Search by ticker or company name
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(
                Q(ticker__icontains=query)
                | Q(name__icontains=query)
                | Q(primary_commodity__icontains=query)
            )

        # Filter by verdict
        verdict_filter = self.request.GET.get("verdict")
        if verdict_filter in VerdictChoice.values:
            qs = qs.filter(scorecards__verdict=verdict_filter, scorecards__is_published=True)

        # Filter by tier
        tier_filter = self.request.GET.get("tier")
        if tier_filter in CompanyTier.values:
            qs = qs.filter(tier=tier_filter)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["verdict_choices"] = VerdictChoice.choices
        ctx["tier_choices"] = CompanyTier.choices
        ctx["active_verdict"] = self.request.GET.get("verdict", "")
        ctx["active_tier"] = self.request.GET.get("tier", "")
        ctx["search_query"] = self.request.GET.get("q", "")
        return ctx


class CompanyDetailView(DetailView):
    model = Company
    template_name = "verdict/company_detail.html"
    context_object_name = "company"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            if re.match(r"^company-\d+$", kwargs.get("slug", "")):
                return redirect("verdict:company_list", permanent=True)
            raise

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["scorecards"] = self.object.scorecards.filter(is_published=True).order_by("-scored_at")
        ctx["latest"] = ctx["scorecards"].first()
        if ctx["latest"]:
            sc = ctx["latest"]
            ctx["latest_factors"] = [
                {"label": "Management Skin-in-the-Game", "score": sc.management_score,  "notes": sc.management_notes},
                {"label": "Project Geology Quality",     "score": sc.geology_score,     "notes": sc.geology_notes},
                {"label": "Capital Structure Health",    "score": sc.capital_score,     "notes": sc.capital_notes},
                {"label": "Catalyst Proximity",          "score": sc.catalyst_score,    "notes": sc.catalyst_notes},
                {"label": "Comparable Acquisition Value", "score": sc.acquisition_score, "notes": sc.acquisition_notes},
            ]
        return ctx


class ScorecardDetailView(DetailView):
    model = VerdictScorecard
    template_name = "verdict/scorecard_detail.html"
    context_object_name = "scorecard"

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        date_str = self.kwargs["date"]
        try:
            scored_date = date_type.fromisoformat(date_str)
        except ValueError:
            raise Http404
        return get_object_or_404(
            VerdictScorecard.objects.filter(is_published=True).select_related("company"),
            company__slug=slug,
            scored_at__date=scored_date,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        sc = self.object
        ctx["factors"] = [
            {"label": "Management Skin-in-the-Game", "score": sc.management_score, "notes": sc.management_notes},
            {"label": "Project Geology Quality",      "score": sc.geology_score,    "notes": sc.geology_notes},
            {"label": "Capital Structure Health",     "score": sc.capital_score,    "notes": sc.capital_notes},
            {"label": "Catalyst Proximity",           "score": sc.catalyst_score,   "notes": sc.catalyst_notes},
            {"label": "Comparable Acquisition Value", "score": sc.acquisition_score,"notes": sc.acquisition_notes},
        ]
        return ctx


def scorecard_pk_redirect(request, slug, pk):
    """301 redirect from old /scorecard/<pk>/ URLs to new /scorecard/<date>/ URLs."""
    scorecard = get_object_or_404(
        VerdictScorecard.objects.filter(is_published=True).select_related("company"),
        pk=pk,
    )
    return redirect(scorecard.get_absolute_url(), permanent=True)


def commodity_list(request, commodity):
    """Verdict-rated companies for a single commodity (gold, silver, copper, ...)."""
    entry = get_commodity(commodity)
    if entry is None:
        raise Http404("Unknown commodity")

    term_filter = Q()
    for term in entry["match_terms"]:
        term_filter |= Q(primary_commodity__icontains=term)

    companies = (
        Company.objects
        .filter(term_filter, scorecards__is_published=True)
        .prefetch_related("scorecards")
        .distinct()
    )

    rows = []
    for c in companies:
        latest = c.latest_verdict
        if latest and latest.is_published:
            rows.append({"company": c, "latest": latest})
    rows.sort(key=lambda r: r["latest"].scored_at, reverse=True)

    return render(request, "verdict/commodity_list.html", {
        "commodity_slug": commodity,
        "commodity": entry,
        "rows": rows,
        "all_commodities": [
            (slug, e["display"]) for slug, e in COMMODITIES.items()
        ],
    })
