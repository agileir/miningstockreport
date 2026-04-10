from django.contrib import admin
from django.utils.html import format_html
from .models import AccreditedInvestor


@admin.register(AccreditedInvestor)
class AccreditedInvestorAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "email", "country", "capital_range",
        "status_display", "referral_source", "assigned_to",
        "last_contacted", "registered_at",
    )
    list_filter  = ("status", "country", "capital_range", "referral_source")
    search_fields = ("first_name", "last_name", "email")
    date_hierarchy = "registered_at"
    ordering = ("-registered_at",)
    readonly_fields = ("consent_timestamp", "consent_ip", "registered_at", "updated_at")
    actions = ["mark_approved", "mark_contacted", "mark_declined"]

    fieldsets = (
        ("Investor", {
            "fields": ("first_name", "last_name", "email", "country", "capital_range", "referral_source"),
        }),
        ("Consent record", {
            "fields": ("confirmed_accredited", "consent_contact", "consent_timestamp", "consent_ip"),
            "description": "These fields are set at registration time and should not be modified.",
        }),
        ("CRM", {
            "fields": ("status", "assigned_to", "last_contacted", "internal_notes"),
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": ("registered_at", "updated_at"),
        }),
    )

    def status_display(self, obj):
        colours = {
            "pending":   ("orange",  "Pending"),
            "approved":  ("green",   "Approved"),
            "contacted": ("#5b9bd5", "Contacted"),
            "declined":  ("grey",    "Declined"),
            "inactive":  ("#888",    "Inactive"),
        }
        colour, label = colours.get(obj.status, ("#888", obj.status))
        return format_html('<strong style="color:{}">{}</strong>', colour, label)
    status_display.short_description = "Status"

    def mark_approved(self, request, queryset):
        queryset.update(status=AccreditedInvestor.Status.APPROVED)
    mark_approved.short_description = "Mark selected as Approved"

    def mark_contacted(self, request, queryset):
        from django.utils import timezone
        queryset.update(status=AccreditedInvestor.Status.CONTACTED, last_contacted=timezone.now())
    mark_contacted.short_description = "Mark selected as Contacted"

    def mark_declined(self, request, queryset):
        queryset.update(status=AccreditedInvestor.Status.DECLINED)
    mark_declined.short_description = "Mark selected as Declined"
