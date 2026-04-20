from django.db import models
from django.urls import reverse


class AutoLink(models.Model):
    """
    Custom keyword phrases that get auto-linked to a target URL
    when they appear in rendered content (blog posts, analyst summaries, etc.).
    Company names and tickers are handled automatically — use this model
    for editorial phrases like "NI 43-101", "Verdict Framework", etc.
    """
    phrase = models.CharField(
        max_length=200, unique=True,
        help_text='Exact phrase to match (case-insensitive). E.g. "NI 43-101", "P/NAV multiple".',
    )
    target_url = models.CharField(
        max_length=500,
        help_text='Relative path (e.g. /about/methodology/) or absolute URL.',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["phrase"]

    def __str__(self):
        return f"{self.phrase} → {self.target_url}"


class CommodityPrice(models.Model):
    """
    Cached commodity prices — updated hourly via management command.
    """
    symbol = models.CharField(max_length=20, unique=True, help_text="Yahoo Finance symbol, e.g. GC=F")
    name = models.CharField(max_length=50, help_text="Display name, e.g. Gold")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    change_pct = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=20, default="/oz", help_text="Unit label, e.g. /oz, /lb")
    sort_order = models.PositiveIntegerField(default=0)
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.name}: ${self.price}"
