from django.shortcuts import render
from django.db.models import Prefetch
from .models import NewsCategory, NewsLink


def news_wire(request):
    active_links = (
        NewsLink.active.get_queryset()
        .order_by("-is_featured", "position", "-published_at")[:10]
    )
    categories = (
        NewsCategory.objects.filter(is_active=True)
        .prefetch_related(
            Prefetch("newslink_set", queryset=active_links, to_attr="active_links")
        )
    )
    featured = NewsLink.active.featured()[:3]
    last_updated = (
        NewsLink.objects.order_by("-created_at")
        .values_list("created_at", flat=True)
        .first()
    )

    return render(request, "news/news_wire.html", {
        "categories": categories,
        "featured_links": featured,
        "last_updated": last_updated,
    })
