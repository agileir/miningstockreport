from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from apps.blog.models import Post
from apps.verdict.commodities import COMMODITIES
from apps.verdict.models import Company
from apps.videos.models import Video


class StaticViewSitemap(Sitemap):
    priority   = 1.0
    changefreq = "weekly"

    # Pages recently edited — emit lastmod so crawlers prioritise a refresh.
    # Update this date when you deploy a meaningful change to one of the
    # listed URLs (or better: move the URL to a model-backed sitemap).
    TOOL_URLS_LASTMOD = timezone.now()

    _TOOL_URLS = {
        "core:tools_index",
        "core:nav_calculator",
        "core:nav_calculator_copper",
        "core:nav_calculator_silver",
        "core:nav_calculator_polymetallic",
        "investors:register",
    }

    def items(self):
        return ["core:home", "core:about", "core:methodology",
                "core:disclaimer",
                "core:tools_index",
                "core:nav_calculator",
                "core:nav_calculator_copper",
                "core:nav_calculator_silver",
                "core:nav_calculator_polymetallic",
                "blog:post_list", "verdict:company_list",
                "videos:video_list", "watchlist:watchlist",
                "news:news_wire",
                "investors:register"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        # Only emit lastmod for URLs we've recently edited. Other static
        # pages don't need a freshness hint.
        if item in self._TOOL_URLS:
            return self.TOOL_URLS_LASTMOD
        return None


class PostSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        )

    def lastmod(self, obj):
        return obj.updated_at

    def priority(self, obj):
        if obj.post_type == "guide":
            return 0.9
        return 0.8


class CompanySitemap(Sitemap):
    changefreq = "weekly"
    priority   = 0.9  # Company pages are high-value — likely to be cited by AI engines

    def items(self):
        return Company.objects.filter(scorecards__is_published=True).distinct()

    def lastmod(self, obj):
        return obj.updated_at


# Dated scorecards (/companies/<slug>/scorecard/YYYY-MM-DD/) are intentionally
# omitted from the sitemap. Each one is noindex, follow — preserved as a public
# accountability record but not submitted for indexing. Ranking signals for a
# company consolidate on the hub page in CompanySitemap.


class VideoSitemap(Sitemap):
    changefreq = "monthly"
    priority   = 0.7

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.published_at


class CommodityListSitemap(Sitemap):
    """One entry per /list-{slug}-stocks/ landing page."""
    changefreq = "weekly"
    priority   = 0.8
    LASTMOD    = timezone.now()

    def items(self):
        return list(COMMODITIES.keys())

    def location(self, item):
        return reverse("commodity_list", kwargs={"commodity": item})

    def lastmod(self, item):
        return self.LASTMOD


sitemaps = {
    "static":            StaticViewSitemap,
    "posts":             PostSitemap,
    "companies":         CompanySitemap,
    "videos":            VideoSitemap,
    "commodity_lists":   CommodityListSitemap,
}
