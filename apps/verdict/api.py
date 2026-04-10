from rest_framework import serializers, viewsets, permissions
from .models import Company, VerdictScorecard


class VerdictScorecardSerializer(serializers.ModelSerializer):
    verdict_label = serializers.CharField(source="get_verdict_display", read_only=True)
    composite_score = serializers.IntegerField(read_only=True)
    composite_score_pct = serializers.IntegerField(read_only=True)

    class Meta:
        model = VerdictScorecard
        fields = [
            "id", "verdict", "verdict_label",
            "management_score", "geology_score", "capital_score",
            "catalyst_score", "acquisition_score",
            "composite_score", "composite_score_pct",
            "nav_per_share", "current_price", "p_nav_multiple",
            "analyst_summary", "scored_at",
        ]


class CompanySerializer(serializers.ModelSerializer):
    latest_verdict = VerdictScorecardSerializer(read_only=True)
    exchange_label = serializers.CharField(source="get_exchange_display", read_only=True)

    class Meta:
        model = Company
        fields = [
            "id", "name", "slug", "ticker", "exchange", "exchange_label",
            "description", "website", "logo", "jurisdiction",
            "primary_commodity", "latest_verdict",
        ]


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.prefetch_related("scorecards").all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class VerdictScorecardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VerdictScorecard.objects.filter(is_published=True).select_related("company")
    serializer_class = VerdictScorecardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        verdict = self.request.query_params.get("verdict")
        if verdict:
            qs = qs.filter(verdict=verdict)
        company = self.request.query_params.get("company")
        if company:
            qs = qs.filter(company__slug=company)
        return qs
