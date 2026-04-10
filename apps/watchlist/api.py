from rest_framework import serializers, viewsets, permissions
from .models import WatchlistItem, PriceCache


class PriceCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceCache
        fields = ["price", "change_pct", "volume", "fetched_at"]


class WatchlistItemSerializer(serializers.ModelSerializer):
    ticker = serializers.CharField(source="company.ticker", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_slug = serializers.CharField(source="company.slug", read_only=True)
    exchange = serializers.CharField(source="company.exchange", read_only=True)
    latest_verdict = serializers.SerializerMethodField()
    price = PriceCacheSerializer(source="company.price_cache", read_only=True)

    class Meta:
        model = WatchlistItem
        fields = [
            "id", "ticker", "company_name", "company_slug", "exchange",
            "status", "thesis", "entry_price", "target_price", "stop_loss",
            "next_catalyst", "catalyst_date", "public_notes",
            "latest_verdict", "price", "added_at",
        ]

    def get_latest_verdict(self, obj):
        v = obj.company.latest_verdict
        if v:
            return {"verdict": v.verdict, "scored_at": v.scored_at}
        return None


class WatchlistItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WatchlistItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        from .models import WatchlistStatus
        return (
            WatchlistItem.objects
            .exclude(status=WatchlistStatus.DROPPED)
            .select_related("company", "company__price_cache")
            .prefetch_related("company__scorecards")
        )
