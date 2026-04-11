from rest_framework import serializers, viewsets, permissions
from django.utils import timezone
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.display_name", read_only=True)
    pillar_slug = serializers.CharField(source="pillar.slug", read_only=True)
    pillar_label = serializers.CharField(source="pillar.name", read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "author_name", "excerpt",
            "pillar_slug", "pillar_label", "tags", "is_premium",
            "featured_image", "published_at", "view_count",
        ]

    def get_tags(self, obj):
        return list(obj.tags.values_list("slug", flat=True))


class PostDetailSerializer(PostSerializer):
    body = serializers.CharField()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ["body", "answer_capsule", "meta_title", "meta_description"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        # Gate body behind premium check
        if instance.is_premium:
            user = request.user if request else None
            if not (user and user.is_authenticated and user.is_premium):
                data["body"] = None
                data["premium_locked"] = True
        return data


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        ).select_related("author")
        pillar = self.request.query_params.get("pillar")
        if pillar:
            qs = qs.filter(pillar__slug=pillar)
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer
