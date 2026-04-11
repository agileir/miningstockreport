from django.views.generic import ListView, DetailView
from .models import Video

# ── Views ──────────────────────────────────────────────────────────────────

class VideoListView(ListView):
    model = Video
    template_name = "videos/video_list.html"
    context_object_name = "videos"
    paginate_by = 12

    def get_queryset(self):
        qs = Video.objects.select_related("pillar")
        pillar_slug = self.kwargs.get("pillar")
        if pillar_slug:
            qs = qs.filter(pillar__slug=pillar_slug)
        return qs


class VideoDetailView(DetailView):
    model = Video
    template_name = "videos/video_detail.html"
    context_object_name = "video"

    def get_queryset(self):
        return Video.objects.select_related("pillar")
