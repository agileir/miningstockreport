from django.contrib import admin
from django.utils.html import format_html
from .models import Jurisdiction


@admin.register(Jurisdiction)
class JurisdictionAdmin(admin.ModelAdmin):
    list_display  = ("name", "country", "region_type", "composite_display",
                     "risk_display", "last_assessed_at", "is_published")
    list_filter   = ("region_type", "country", "is_published")
    search_fields = ("name", "country")
    readonly_fields = ("composite_display", "risk_display", "created_at", "updated_at")
    fieldsets = (
        ("Identity", {
            "fields": ("name", "country", "country_code", "region_type", "is_published"),
        }),
        ("Permitting (Factor 1)",     {"fields": ("permitting_score",     "permitting_notes")}),
        ("Fiscal Regime (Factor 2)",  {"fields": ("fiscal_score",         "fiscal_notes")}),
        ("Political & Security (Factor 3)", {"fields": ("political_score", "political_notes")}),
        ("Infrastructure (Factor 4)", {"fields": ("infrastructure_score", "infrastructure_notes")}),
        ("Community & ESG (Factor 5)", {"fields": ("community_score",     "community_notes")}),
        ("Narrative", {"fields": ("summary", "whats_changed", "last_assessed_at")}),
        ("Computed", {"fields": ("composite_display", "risk_display")}),
        ("SEO & Open Graph", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "og_image_alt"),
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    def composite_display(self, obj):
        if obj.pk is None:
            return "—"
        return f"{obj.composite_score}/25 ({obj.composite_score_pct}%)"
    composite_display.short_description = "Composite"

    def risk_display(self, obj):
        if obj.pk is None:
            return "—"
        colours = {
            "LOW": "#4ade80", "MODERATE": "#60a5fa",
            "ELEVATED": "#ffc107", "HIGH": "#f87171", "EXTREME": "#dc2626",
        }
        c = colours.get(obj.risk_label, "#888")
        return format_html('<strong style="color:{}">{}</strong>', c, obj.risk_label_display)
    risk_display.short_description = "Risk Level"
