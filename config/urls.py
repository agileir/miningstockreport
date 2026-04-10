from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import sitemaps
from apps.core.views import robots_txt, llms_txt, handler404, handler500

handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # SEO essentials
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt",  robots_txt,  name="robots_txt"),
    path("llms.txt",    llms_txt,    name="llms_txt"),

    # Frontend apps — note URL prefixes chosen for topical SEO signal
    path("",            include("apps.core.urls",      namespace="core")),
    path("analysis/",   include("apps.blog.urls",      namespace="blog")),
    path("videos/",     include("apps.videos.urls",    namespace="videos")),
    path("companies/",  include("apps.verdict.urls",   namespace="verdict")),
    path("watchlist/",  include("apps.watchlist.urls", namespace="watchlist")),
    path("accounts/",   include("apps.accounts.urls",  namespace="accounts")),
    path("subscribe/",  include("apps.leads.urls",     namespace="leads")),
    path("investors/",  include("apps.investors.urls", namespace="investors")),

    # REST API (v1)
    path("api/v1/",     include("config.api_urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
