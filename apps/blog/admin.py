from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ("title", "pillar", "author", "status", "is_premium",
                     "word_count", "published_at", "view_count")
    list_filter   = ("status", "pillar", "is_premium")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering       = ("-published_at",)
    raw_id_fields  = ("author",)
    readonly_fields = ("word_count", "view_count")

    fieldsets = (
        (None, {
            "fields": ("title", "slug", "author", "status", "published_at"),
        }),
        ("Content", {
            "fields": ("excerpt", "key_takeaways", "body", "faq_items",
                       "featured_image", "featured_image_alt"),
        }),
        ("Classification", {
            "fields": ("pillar", "tags", "is_premium"),
        }),
        ("SEO & Open Graph", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "og_image_alt"),
            "description": (
                "meta_title: 50–60 chars. meta_description: 120–155 chars. "
                "og_image: 1200×630px. Leave blank to auto-derive from title/excerpt."
            ),
        }),
        ("Stats", {
            "classes": ("collapse",),
            "fields": ("word_count", "view_count"),
        }),
    )
