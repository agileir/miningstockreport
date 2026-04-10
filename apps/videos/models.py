from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from apps.blog.models import ContentPillar
from apps.core.seo import SEOMixin


class Video(SEOMixin, models.Model):
    title       = models.CharField(max_length=250)
    slug        = AutoSlugField(populate_from="title", unique=True, always_update=False)
    youtube_id  = models.CharField(max_length=20, unique=True,
        help_text="11-character YouTube video ID from the URL.")
    description = models.TextField(blank=True)
    pillar      = models.CharField(max_length=30, choices=ContentPillar.choices,
        default=ContentPillar.DUE_DILIGENCE, db_index=True)
    is_featured = models.BooleanField(default=False)
    is_premium  = models.BooleanField(default=False)
    thumbnail_url = models.URLField(blank=True,
        help_text="Leave blank to auto-derive from YouTube ID.")
    published_at = models.DateTimeField(db_index=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("videos:video_detail", kwargs={"slug": self.slug})

    @property
    def embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}"

    @property
    def thumbnail(self):
        return self.thumbnail_url or f"https://img.youtube.com/vi/{self.youtube_id}/maxresdefault.jpg"

    @property
    def seo_title(self):
        return self.get_seo_title(self.title)

    @property
    def seo_description(self):
        return self.get_seo_description(self.description[:160] if self.description else "")
