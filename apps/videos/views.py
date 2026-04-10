from django.views.generic import ListView, DetailView
from .models import Video

# ── Views ──────────────────────────────────────────────────────────────────

class VideoListView(ListView):
    model = Video
    template_name = "videos/video_list.html"
    context_object_name = "videos"
    paginate_by = 12

    def get_queryset(self):
        qs = Video.objects.all()
        pillar = self.kwargs.get("pillar")
        if pillar:
            qs = qs.filter(pillar=pillar)
        return qs


class VideoDetailView(DetailView):
    model = Video
    template_name = "videos/video_detail.html"
    context_object_name = "video"
