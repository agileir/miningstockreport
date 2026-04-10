from django.contrib import admin
from .models import WatchlistItem, PriceCache


@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = (
        "company", "status", "entry_price", "target_price",
        "stop_loss", "next_catalyst", "catalyst_date", "added_at",
    )
    list_filter = ("status",)
    search_fields = ("company__name", "company__ticker")
    raw_id_fields = ("company",)
    fieldsets = (
        ("Company", {"fields": ("company", "status")}),
        ("Thesis & Pricing", {"fields": ("thesis", "entry_price", "target_price", "stop_loss", "position_size_pct")}),
        ("Catalysts", {"fields": ("next_catalyst", "catalyst_date")}),
        ("Notes", {"fields": ("public_notes", "private_notes")}),
        ("Timestamps", {"fields": ("exited_at",)}),
    )


@admin.register(PriceCache)
class PriceCacheAdmin(admin.ModelAdmin):
    list_display = ("company", "price", "change_pct", "volume", "fetched_at")
    readonly_fields = ("fetched_at",)
