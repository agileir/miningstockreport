from django.conf import settings
from apps.blog.models import Pillar
from apps.core.models import CommodityPrice
from apps.verdict.commodities import all_commodities


def site_context(request):
    """Injects global site metadata into every template context."""
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_URL": settings.SITE_URL,
        "YOUTUBE_CHANNEL_URL": settings.YOUTUBE_CHANNEL_URL,
        "TWITTER_URL": settings.TWITTER_URL,
        "nav_pillars": Pillar.objects.filter(is_active=True),
        "commodity_prices": CommodityPrice.objects.all(),
        "footer_commodity_lists": all_commodities(),
    }
