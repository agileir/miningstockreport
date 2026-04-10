from rest_framework import serializers, viewsets, permissions
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    pillar_label = serializers.CharField(source="get_pillar_display", read_only=True)

    class Meta:
        model = Video
        fields = [
            "id", "title", "slug", "youtube_id", "embed_url", "thumbnail",
            "description", "pillar", "pillar_label", "is_featured",
            "is_premium", "published_at",
        ]


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Video.objects.all()
        pillar = self.request.query_params.get("pillar")
        if pillar:
            qs = qs.filter(pillar=pillar)
        featured = self.request.query_params.get("featured")
        if featured:
            qs = qs.filter(is_featured=True)
        return qs
