from django.db import models


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
