from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "membership_tier", "is_premium", "date_joined")
    list_filter = ("membership_tier", "is_staff", "is_active")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Membership", {"fields": ("membership_tier", "membership_expires", "stripe_customer_id")}),
        ("Profile", {"fields": ("bio", "avatar")}),
    )
