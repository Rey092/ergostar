"""Subscription Plan Admin."""

from django.contrib import admin
from unfold.admin import ModelAdmin

from admin.core.models import SubscriptionPlansUnfold


@admin.register(SubscriptionPlansUnfold)
class SubscriptionPlansUnfoldAdmin(ModelAdmin):
    """Subscription Plan Admin."""

    list_display = (
        "title",
        "subtitle",
        "monthly_price",
        "annual_price",
        "monthly_requests_limit",
        "rate_limit",
        "rate_period",
        "is_public",
    )
    search_fields = ("title", "subtitle")
    list_filter = ("is_public",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "subtitle",
                    "monthly_price",
                    "annual_price",
                    "monthly_requests_limit",
                    "rate_limit",
                    "rate_period",
                    "is_public",
                ),
            },
        ),
        (
            "Date Information",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
