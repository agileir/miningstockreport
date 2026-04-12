from django.contrib import admin
from django.utils.html import format_html
from .models import Company, VerdictScorecard


class VerdictScorecardInline(admin.TabularInline):
    model  = VerdictScorecard
    extra  = 0
    fields = ("scored_at", "verdict", "composite_score_display", "is_published")
    readonly_fields = ("composite_score_display",)

    def composite_score_display(self, obj):
        return f"{obj.composite_score}/25 ({obj.composite_score_pct}%)" if obj.pk else "—"
    composite_score_display.short_description = "Score"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display   = ("ticker", "name", "exchange", "primary_commodity",
                      "jurisdiction", "data_filled", "needs_research", "latest_verdict_display")
    list_editable  = ("needs_research",)
    list_filter    = ("exchange", "primary_commodity", "data_filled", "needs_research")
    search_fields  = ("name", "ticker")
    inlines        = [VerdictScorecardInline]
    actions        = ["flag_for_research", "clear_research_flag"]

    fieldsets = (
        ("Quick Add", {"fields": ("ticker", "exchange")}),
        ("Company Details (filled by AI agent)", {
            "classes": ("collapse",),
            "fields": ("name", "exchange", "description", "website", "logo",
                       "jurisdiction", "primary_commodity", "market_cap_cad"),
        }),
        ("Agent Flags", {"fields": ("data_filled", "needs_research")}),
        ("SEO & Open Graph", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "og_image_alt"),
        }),
    )

    def latest_verdict_display(self, obj):
        v = obj.latest_verdict
        if not v:
            return "—"
        colours = {"BUY": "green", "WATCH": "orange", "AVOID": "red"}
        return format_html(
            '<strong style="color:{}">{}</strong>',
            colours.get(v.verdict, "grey"), v.verdict,
        )
    latest_verdict_display.short_description = "Latest Verdict"

    @admin.action(description="Flag for AI research")
    def flag_for_research(self, request, queryset):
        queryset.update(needs_research=True)

    @admin.action(description="Clear research flag")
    def clear_research_flag(self, request, queryset):
        queryset.update(needs_research=False)


@admin.register(VerdictScorecard)
class VerdictScorecardAdmin(admin.ModelAdmin):
    list_display  = ("company", "verdict", "composite_score_display",
                     "p_nav_multiple", "is_published", "scored_at")
    list_filter   = ("verdict", "is_published")
    search_fields = ("company__name", "company__ticker")
    date_hierarchy = "scored_at"
    readonly_fields = ("composite_score_display", "p_nav_multiple")

    fieldsets = (
        ("Company & Verdict",  {"fields": ("company", "verdict", "analyst_summary", "scored_at", "is_published")}),
        ("Factor 1 — Management",   {"fields": ("management_score",   "management_notes")}),
        ("Factor 2 — Geology",      {"fields": ("geology_score",      "geology_notes")}),
        ("Factor 3 — Capital",      {"fields": ("capital_score",      "capital_notes")}),
        ("Factor 4 — Catalyst",     {"fields": ("catalyst_score",     "catalyst_notes")}),
        ("Factor 5 — Acquisition",  {"fields": ("acquisition_score",  "acquisition_notes")}),
        ("Valuation",  {"fields": ("nav_per_share", "current_price", "p_nav_multiple")}),
        ("SEO & Open Graph", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "og_image_alt"),
        }),
    )

    def composite_score_display(self, obj):
        return f"{obj.composite_score}/25 ({obj.composite_score_pct}%)"
    composite_score_display.short_description = "Composite Score"
