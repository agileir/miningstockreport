from django.db import models
from apps.verdict.models import Company


class WatchlistStatus(models.TextChoices):
    WATCHING = "watching", "Watching"
    POSITION = "position", "In Position"
    SOLD = "sold", "Sold / Exited"
    DROPPED = "dropped", "Dropped from Watchlist"


class WatchlistItem(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="watchlist_item")
    status = models.CharField(max_length=10, choices=WatchlistStatus.choices, default=WatchlistStatus.WATCHING, db_index=True)

    # Analyst thesis
    thesis = models.TextField(help_text="Why this is on the watchlist.")
    entry_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    position_size_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Portfolio allocation % (for accountability tracking).",
    )

    # Catalyst tracking
    next_catalyst = models.CharField(max_length=200, blank=True, help_text="e.g. Q3 drill results expected")
    catalyst_date = models.DateField(null=True, blank=True)

    # Public notes (shown on site)
    public_notes = models.TextField(blank=True)
    # Private notes (admin only)
    private_notes = models.TextField(blank=True)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.company.ticker} — {self.status}"


class PriceCache(models.Model):
    """
    Lightweight price cache — populate via management command or cron.
    Avoids live API calls on page render.
    """
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="price_cache")
    price = models.DecimalField(max_digits=10, decimal_places=4)
    change_pct = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.ticker}: ${self.price}"
