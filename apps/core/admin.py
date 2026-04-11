from django.contrib import admin
from apps.core.models import CommodityPrice


@admin.register(CommodityPrice)
class CommodityPriceAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol", "price", "change_pct", "unit", "fetched_at"]
    readonly_fields = ["fetched_at"]
