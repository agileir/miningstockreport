import hashlib
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from django.db import models
from django.utils import timezone


def normalize_url(url):
    """Strip tracking params and normalize for dedup."""
    parsed = urlparse(url.strip().lower())
    params = {k: v for k, v in parse_qs(parsed.query).items()
              if not k.startswith("utm_")}
    clean_query = urlencode(params, doseq=True)
    return urlunparse(parsed._replace(query=clean_query, fragment=""))


def hash_url(url):
    return hashlib.sha256(normalize_url(url).encode()).hexdigest()


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class, e.g. bi-gem")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "news categories"

    def __str__(self):
        return self.name


class ActiveNewsManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(is_active=True)
            .filter(models.Q(expires_at__gt=now) | models.Q(expires_at__isnull=True))
        )

    def featured(self):
        return self.get_queryset().filter(is_featured=True).order_by("-published_at")

    def by_category(self, slug):
        return self.get_queryset().filter(category__slug=slug)


class AddedBy(models.TextChoices):
    AGENT = "agent", "Agent"
    MANUAL = "manual", "Manual"


class NewsLink(models.Model):
    headline = models.TextField()
    url = models.URLField(max_length=500)
    url_hash = models.CharField(max_length=64, unique=True, db_index=True, editable=False)
    source_name = models.CharField(max_length=100)
    category = models.ForeignKey(
        NewsCategory, on_delete=models.SET_NULL, null=True, blank=True,
    )
    snippet = models.TextField(blank=True)

    is_featured = models.BooleanField(default=False, db_index=True)
    is_breaking = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    added_by = models.CharField(max_length=10, choices=AddedBy.choices, default=AddedBy.MANUAL)
    position = models.PositiveIntegerField(default=0)

    published_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveNewsManager()

    class Meta:
        ordering = ["-is_featured", "position", "-published_at"]
        indexes = [
            models.Index(fields=["is_active", "category", "-published_at"]),
            models.Index(fields=["is_active", "is_featured", "-published_at"]),
        ]

    def __str__(self):
        return self.headline[:80]

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = hash_url(self.url)
        super().save(*args, **kwargs)
