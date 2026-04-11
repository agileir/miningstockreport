from django.db import models
from django.urls import reverse
from django.conf import settings
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from apps.core.seo import SEOMixin


class Pillar(models.Model):
    """Content pillar — editable from admin, designed around SEO/GEO keywords."""
    name = models.CharField(max_length=100, help_text="Display name (e.g. 'Due Diligence')")
    slug = models.SlugField(
        max_length=100, unique=True,
        help_text="URL-safe identifier. Auto-generated from name if left blank. Edit to target specific SEO keywords.",
    )
    description = models.TextField(
        blank=True,
        help_text="SEO-focused description. Used in pillar landing page meta description.",
    )
    seo_title = models.CharField(
        max_length=70, blank=True,
        help_text="Custom meta title for pillar pages (50-60 chars ideal). Leave blank to auto-derive.",
    )
    sort_order = models.PositiveIntegerField(
        default=0, help_text="Controls display order in nav, footer, and filters. Lower = first.",
    )
    is_active = models.BooleanField(default=True, help_text="Inactive pillars are hidden from the site.")

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:post_list_by_pillar", kwargs={"pillar": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(SEOMixin, models.Model):

    class Status(models.TextChoices):
        DRAFT     = "draft",     "Draft"
        PUBLISHED = "published", "Published"

    title  = models.CharField(max_length=250)
    slug   = AutoSlugField(populate_from="title", unique=True, always_update=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="posts",
    )
    excerpt = models.TextField(
        max_length=500,
        help_text="Short summary shown in listings and used as fallback meta description.",
    )
    answer_capsule = models.TextField(
        blank=True,
        help_text="2-3 sentence direct answer to the post's core question. "
                  "Displayed prominently before the body. AI platforms extract this for citations. "
                  'E.g. "Based on our Verdict Framework, XYZ scores 19/25 and receives a BUY rating."',
    )
    key_takeaways = models.JSONField(
        default=list, blank=True,
        help_text='List of short bullet strings. E.g. ["Score 19/25", "P/NAV 0.18x"]. Rendered at top of post and in schema.',
    )
    body = models.TextField(help_text="Supports Markdown or plain HTML.")
    faq_items = models.JSONField(
        default=list, blank=True,
        help_text='List of {"question": "...", "answer": "..."} objects. Rendered as FAQ accordion + FAQPage JSON-LD.',
    )
    featured_image     = models.ImageField(upload_to="blog/images/%Y/%m/", blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True)
    pillar = models.ForeignKey(
        Pillar, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="posts", db_index=True,
    )
    tags       = TaggableManager(blank=True)
    is_premium = models.BooleanField(default=False)
    status       = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    word_count = models.PositiveIntegerField(default=0, help_text="Auto-calculated on save.")

    class Meta:
        ordering = ["-published_at"]
        indexes  = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["pillar", "status"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def seo_title(self):
        return self.get_seo_title(self.title)

    @property
    def seo_description(self):
        return self.get_seo_description(self.excerpt)

    @property
    def reading_time(self):
        words = self.word_count or len(self.body.split())
        return max(1, round(words / 200))

    def save(self, *args, **kwargs):
        import re
        plain = re.sub(r"<[^>]+>", "", self.body)
        self.word_count = len(plain.split())
        super().save(*args, **kwargs)

    def increment_views(self):
        Post.objects.filter(pk=self.pk).update(view_count=models.F("view_count") + 1)
