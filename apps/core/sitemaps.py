from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from apps.blog.models import Post
from apps.verdict.models import Company, VerdictScorecard
from apps.videos.models import Video


class StaticViewSitemap(Sitemap):
    priority   = 1.0
    changefreq = "weekly"

    def items(self):
        return ["core:home", "core:about", "core:methodology",
                "core:disclaimer",
                "blog:post_list", "verdict:company_list",
                "videos:video_list", "watchlist:watchlist",
                "news:news_wire"]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority   = 0.8

    def items(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        )

    def lastmod(self, obj):
        return obj.updated_at


class CompanySitemap(Sitemap):
    changefreq = "weekly"
    priority   = 0.9  # Company pages are high-value — likely to be cited by AI engines

    def items(self):
        return Company.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class VideoSitemap(Sitemap):
    changefreq = "monthly"
    priority   = 0.7

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.published_at


sitemaps = {
    "static":    StaticViewSitemap,
    "posts":     PostSitemap,
    "companies": CompanySitemap,
    "videos":    VideoSitemap,
}
