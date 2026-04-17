import re

from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Company, VerdictScorecard, VerdictChoice


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

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["verdict_choices"] = VerdictChoice.choices
        ctx["active_verdict"] = self.request.GET.get("verdict", "")
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
                ("Management",  sc.management_score),
                ("Geology",     sc.geology_score),
                ("Capital",     sc.capital_score),
                ("Catalyst",    sc.catalyst_score),
                ("Acquisition", sc.acquisition_score),
            ]
        return ctx


class ScorecardDetailView(DetailView):
    model = VerdictScorecard
    template_name = "verdict/scorecard_detail.html"
    context_object_name = "scorecard"
    queryset = VerdictScorecard.objects.filter(is_published=True).select_related("company")

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", "")
        if re.match(r"^company-\d+$", slug):
            try:
                scorecard = self.get_queryset().get(pk=kwargs["pk"])
                return redirect(scorecard.get_absolute_url(), permanent=True)
            except VerdictScorecard.DoesNotExist:
                return redirect("verdict:company_list", permanent=True)
        return super().get(request, *args, **kwargs)

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
