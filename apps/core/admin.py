from django.contrib import admin
from apps.core.models import AutoLink, CommodityPrice


@admin.register(AutoLink)
class AutoLinkAdmin(admin.ModelAdmin):
    list_display = ["phrase", "target_url", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["phrase"]


@admin.register(CommodityPrice)
class CommodityPriceAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol", "price", "change_pct", "unit", "sort_order", "fetched_at"]
    list_editable = ["sort_order"]
    readonly_fields = ["fetched_at"]
