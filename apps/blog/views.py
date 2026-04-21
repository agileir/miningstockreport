from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Post, Pillar


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        qs = Post.objects.filter(status=Post.Status.PUBLISHED, published_at__lte=timezone.now())
        pillar_slug = self.kwargs.get("pillar")
        if pillar_slug:
            qs = qs.filter(pillar__slug=pillar_slug)
        tag = self.request.GET.get("tag")
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs.select_related("author", "pillar")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pillars"] = Pillar.objects.filter(is_active=True)
        pillar_slug = self.kwargs.get("pillar", "")
        ctx["active_pillar"] = pillar_slug
        if pillar_slug:
            ctx["pillar_obj"] = Pillar.objects.filter(slug=pillar_slug).first()
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        ).select_related("author", "pillar")

    def get_template_names(self):
        if self.object.post_type == "listicle":
            return ["blog/post_detail_listicle.html"]
        if self.object.post_type == "guide":
            return ["blog/post_detail_guide.html"]
        return ["blog/post_detail.html"]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().get(request, *args, **kwargs)
        self.object.increment_views()
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object
        ctx["is_locked"] = post.is_premium and not (
            self.request.user.is_authenticated and self.request.user.is_premium
        )
        ctx["related_posts"] = (
            Post.objects.filter(
                status=Post.Status.PUBLISHED,
                pillar=post.pillar,
            )
            .exclude(pk=post.pk)
            .select_related("pillar")
            .order_by("-published_at")[:3]
        )
        return ctx
