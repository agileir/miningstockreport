from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import WatchlistItem, WatchlistStatus

# ── Views ──────────────────────────────────────────────────────────────────

class WatchlistView(ListView):
    model = WatchlistItem
    template_name = "watchlist/watchlist.html"
    context_object_name = "items"

    def get_queryset(self):
        return (
            WatchlistItem.objects
            .exclude(status=WatchlistStatus.DROPPED)
            .select_related("company", "company__price_cache")
            .prefetch_related("company__scorecards")
            .order_by("status", "-added_at")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["watching"] = [i for i in ctx["items"] if i.status == WatchlistStatus.WATCHING]
        ctx["in_position"] = [i for i in ctx["items"] if i.status == WatchlistStatus.POSITION]
        ctx["sold"] = (
            WatchlistItem.objects
            .filter(status=WatchlistStatus.SOLD)
            .select_related("company")
            .order_by("-exited_at")[:10]
        )
        return ctx
