from django.contrib import admin
from .models import Subscriber, LeadMagnet


@admin.register(LeadMagnet)
class LeadMagnetAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "subscriber_count", "created_at")

    def subscriber_count(self, obj):
        return obj.subscribers.count()
    subscriber_count.short_description = "Subscribers"


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "source", "lead_magnet", "mailchimp_synced", "is_active", "subscribed_at")
    list_filter = ("source", "is_active", "mailchimp_synced")
    search_fields = ("email", "first_name")
    date_hierarchy = "subscribed_at"
    ordering = ("-subscribed_at",)
    actions = ["mark_inactive"]

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected subscribers as inactive"
