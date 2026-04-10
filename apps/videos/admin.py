from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "youtube_id", "pillar", "is_featured", "is_premium", "published_at")
    list_filter = ("pillar", "is_featured", "is_premium")
    search_fields = ("title", "description", "youtube_id")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
