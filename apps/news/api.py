from rest_framework import serializers, viewsets, permissions
from .models import NewsLink


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
