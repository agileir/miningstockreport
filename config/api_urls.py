"""
API v1 URL configuration
All endpoints are prefixed with /api/v1/
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.blog.api import PostViewSet
from apps.videos.api import VideoViewSet
from apps.verdict.api import CompanyViewSet, VerdictScorecardViewSet
from apps.watchlist.api import WatchlistItemViewSet
from apps.leads.api import SubscriberCreateView
from apps.investors.api import AccreditedInvestorCreateView
from apps.news.api import NewsLinkViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"videos", VideoViewSet, basename="video")
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"verdicts", VerdictScorecardViewSet, basename="verdict")
router.register(r"watchlist", WatchlistItemViewSet, basename="watchlist")
router.register(r"news", NewsLinkViewSet, basename="news")

urlpatterns = [
    # JWT auth (for mobile app)
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Subscriber email capture
    path("subscribe/", SubscriberCreateView.as_view(), name="api-subscribe"),
    path("investors/", AccreditedInvestorCreateView.as_view(), name="api-investors"),

    # Router-generated endpoints
    path("", include(router.urls)),
]
