from django.db import models


class LeadMagnet(models.Model):
    """Downloadable assets used to capture emails."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="lead_magnets/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    """Email capture. Source tracks which lead magnet or page drove signup."""

    class Source(models.TextChoices):
        HOMEPAGE = "homepage", "Homepage"
        BLOG = "blog", "Blog Post"
        VIDEO = "video", "Video Page"
        VERDICT = "verdict", "Verdict / Scorecard"
        WATCHLIST = "watchlist", "Watchlist"
        LEAD_MAGNET = "lead_magnet", "Lead Magnet"
        API = "api", "API / Mobile App"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.HOMEPAGE)
    lead_magnet = models.ForeignKey(
        LeadMagnet,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="subscribers",
    )
    mailchimp_synced = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
