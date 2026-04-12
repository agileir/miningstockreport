from django.conf import settings
from django.utils import timezone
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company, VerdictScorecard, VerdictChoice


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


class ScorecardIngestView(APIView):
    """
    POST /api/v1/verdicts/ingest/
    Accepts a scorecard JSON from the AI research agent.
    Secured by X-Ingest-Token header (same token as news ingest).
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    SCORE_FIELDS = [
        "management_score", "geology_score", "capital_score",
        "catalyst_score", "acquisition_score",
    ]
    NOTE_FIELDS = [
        "management_notes", "geology_notes", "capital_notes",
        "catalyst_notes", "acquisition_notes",
    ]

    def post(self, request):
        token = getattr(settings, "NEWS_INGEST_TOKEN", "")
        if not token:
            return Response({"error": "Ingest token not configured"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if request.headers.get("X-Ingest-Token", "") != token:
            return Response({"error": "Invalid or missing token"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        ticker = (data.get("ticker") or "").strip()
        if not ticker:
            return Response({"error": "ticker is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(ticker__iexact=ticker)
        except Company.DoesNotExist:
            return Response({"error": f"Company with ticker '{ticker}' not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate scores
        for field in self.SCORE_FIELDS:
            val = data.get(field)
            if val is None or not (1 <= int(val) <= 5):
                return Response({"error": f"{field} must be 1-5"}, status=status.HTTP_400_BAD_REQUEST)

        verdict = (data.get("verdict") or "").upper()
        if verdict not in VerdictChoice.values:
            return Response({"error": f"verdict must be one of: {', '.join(VerdictChoice.values)}"}, status=status.HTTP_400_BAD_REQUEST)

        confidence = (data.get("confidence") or "low").lower()
        is_published = confidence == "high"

        scorecard = VerdictScorecard.objects.create(
            company=company,
            management_score=int(data["management_score"]),
            management_notes=data.get("management_notes", ""),
            geology_score=int(data["geology_score"]),
            geology_notes=data.get("geology_notes", ""),
            capital_score=int(data["capital_score"]),
            capital_notes=data.get("capital_notes", ""),
            catalyst_score=int(data["catalyst_score"]),
            catalyst_notes=data.get("catalyst_notes", ""),
            acquisition_score=int(data["acquisition_score"]),
            acquisition_notes=data.get("acquisition_notes", ""),
            verdict=verdict,
            analyst_summary=data.get("analyst_summary", ""),
            nav_per_share=data.get("nav_per_share"),
            current_price=data.get("current_price"),
            is_published=is_published,
            scored_at=timezone.now(),
        )

        # Clear the research flag
        company.needs_research = False
        company.save(update_fields=["needs_research"])

        return Response({
            "id": scorecard.id,
            "company": company.ticker,
            "verdict": scorecard.verdict,
            "composite_score": scorecard.composite_score,
            "is_published": is_published,
            "confidence": confidence,
        }, status=status.HTTP_201_CREATED)
