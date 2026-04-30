from collections import OrderedDict

from django.views.generic import ListView, DetailView

from .models import Jurisdiction


class JurisdictionListView(ListView):
    model = Jurisdiction
    template_name = "jurisdictions/index.html"
    context_object_name = "jurisdictions"

    def get_queryset(self):
        return Jurisdiction.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Group by country, preserving ordering
        grouped = OrderedDict()
        for j in ctx["jurisdictions"]:
            grouped.setdefault(j.country, []).append(j)
        ctx["grouped"] = grouped
        # Flat sortable rows for the table view
        ctx["rows"] = list(ctx["jurisdictions"])
        return ctx


class JurisdictionDetailView(DetailView):
    model = Jurisdiction
    template_name = "jurisdictions/detail.html"
    context_object_name = "jurisdiction"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Jurisdiction.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Companies operating primarily in this jurisdiction (FK lookup)
        ctx["companies"] = list(self.object.companies.all().order_by("ticker"))
        # Sibling jurisdictions in the same country
        ctx["siblings"] = list(
            Jurisdiction.objects
            .filter(country=self.object.country, is_published=True)
            .exclude(pk=self.object.pk)
            .order_by("name")
        )
        return ctx
