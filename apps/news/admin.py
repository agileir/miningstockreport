from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import NewsCategory, NewsLink


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon_class", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(NewsLink)
class NewsLinkAdmin(admin.ModelAdmin):
    list_display = [
        "headline", "source_name", "category", "is_featured",
        "is_breaking", "is_active", "added_by", "published_at", "click_count",
    ]
    list_filter = ["category", "is_featured", "is_breaking", "is_active", "added_by"]
    list_editable = ["is_featured", "is_breaking", "is_active", "position"]
    search_fields = ["headline", "url", "source_name"]
    readonly_fields = ["url_hash", "click_count", "created_at", "updated_at"]

    fieldsets = (
        (None, {
            "fields": ("headline", "url", "source_name", "category"),
        }),
        ("Content", {
            "fields": ("snippet",),
        }),
        ("Display", {
            "fields": ("is_featured", "is_breaking", "is_active", "position", "added_by"),
        }),
        ("Expiry", {
            "fields": ("expires_at",),
        }),
        ("Metadata", {
            "classes": ("collapse",),
            "fields": ("url_hash", "click_count", "created_at", "updated_at"),
        }),
    )

    actions = ["mark_featured", "remove_featured", "deactivate_selected", "extend_expiry_24h"]

    @admin.action(description="Mark as featured")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Remove featured")
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)

    @admin.action(description="Deactivate selected")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Extend expiry by 24h")
    def extend_expiry_24h(self, request, queryset):
        now = timezone.now()
        for link in queryset:
            base = link.expires_at if link.expires_at and link.expires_at > now else now
            link.expires_at = base + timedelta(hours=24)
            link.save(update_fields=["expires_at"])
