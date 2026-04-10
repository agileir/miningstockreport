from django.conf import settings


def site_context(request):
    """Injects global site metadata into every template context."""
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_URL": settings.SITE_URL,
        "YOUTUBE_CHANNEL_URL": settings.YOUTUBE_CHANNEL_URL,
        "TWITTER_URL": settings.TWITTER_URL,
    }
