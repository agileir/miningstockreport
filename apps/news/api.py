from datetime import timedelta

from django.conf import settings
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import NewsCategory, NewsLink, AddedBy, hash_url


MAX_FEATURED = 3


class NewsLinkSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True, default=None)
    category_slug = serializers.CharField(source="category.slug", read_only=True, default=None)

    class Meta:
        model = NewsLink
        fields = [
            "id", "headline", "url", "source_name",
            "category_name", "category_slug", "snippet",
            "is_featured", "is_breaking", "published_at",
        ]


class NewsLinkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsLinkSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = NewsLink.active.get_queryset().select_related("category")
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__slug=category)
        return qs


class NewsIngestView(APIView):
    """
    POST /api/v1/news/ingest/
    Accepts a JSON array of news items, secured by a bearer token.

    Headers:
        Authorization: Bearer <NEWS_INGEST_TOKEN>

    Body: [{"headline": "...", "url": "...", "source_name": "...",
            "category_slug": "...", "snippet": "...",
            "is_featured": false, "is_breaking": false}]
    """
    authentication_classes = []  # Skip JWT — we use our own token
    permission_classes = [permissions.AllowAny]

    SHORT_EXPIRY_SLUGS = {"market-macro"}
    DEFAULT_EXPIRY_HOURS = 48
    SHORT_EXPIRY_HOURS = 24
    FEATURED_EXPIRY_HOURS = 72

    def post(self, request):
        # Token auth via X-Ingest-Token header
        token = getattr(settings, "NEWS_INGEST_TOKEN", "")
        if not token:
            return Response(
                {"error": "NEWS_INGEST_TOKEN not configured"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        provided = request.headers.get("X-Ingest-Token", "")
        if provided != token:
            return Response(
                {"error": "Invalid or missing token"},
                status=status.HTTP_403_FORBIDDEN,
            )

        items = request.data
        if not isinstance(items, list):
            return Response(
                {"error": "Body must be a JSON array"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = timezone.now()
        categories = {c.slug: c for c in NewsCategory.objects.all()}
        created = 0
        skipped = 0

        for item in items:
            url = (item.get("url") or "").strip()
            headline = (item.get("headline") or "").strip()
            if not url or not headline:
                continue

            url_hash_val = hash_url(url)
            if NewsLink.objects.filter(url_hash=url_hash_val).exists():
                skipped += 1
                continue

            cat_slug = item.get("category_slug", "")
            category = categories.get(cat_slug)
            is_featured = item.get("is_featured", False)

            if is_featured:
                expiry_hours = self.FEATURED_EXPIRY_HOURS
            elif cat_slug in self.SHORT_EXPIRY_SLUGS:
                expiry_hours = self.SHORT_EXPIRY_HOURS
            else:
                expiry_hours = self.DEFAULT_EXPIRY_HOURS

            NewsLink.objects.create(
                headline=headline,
                url=url,
                url_hash=url_hash_val,
                source_name=item.get("source_name", ""),
                category=category,
                snippet=item.get("snippet", ""),
                is_featured=is_featured,
                is_breaking=item.get("is_breaking", False),
                added_by=AddedBy.AGENT,
                expires_at=now + timedelta(hours=expiry_hours),
            )
            created += 1

        # Auto-demote oldest featured if over limit
        featured_ids = list(
            NewsLink.active.featured().values_list("id", flat=True)
        )
        demoted = 0
        if len(featured_ids) > MAX_FEATURED:
            demote_ids = featured_ids[MAX_FEATURED:]
            NewsLink.objects.filter(id__in=demote_ids).update(is_featured=False)
            demoted = len(demote_ids)

        return Response({
            "created": created,
            "skipped": skipped,
            "demoted": demoted,
        }, status=status.HTTP_201_CREATED)
