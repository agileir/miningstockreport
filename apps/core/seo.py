from django.db import models


class SEOMixin(models.Model):
    """
    Abstract mixin providing consistent SEO fields across all content models.
    Inherit from this on any model that has a public-facing detail page.
    """
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Page title tag. 50–60 chars ideal. Leave blank to auto-derive.",
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Meta description. 120–155 chars ideal. Leave blank to auto-derive.",
    )
    og_image = models.ImageField(
        upload_to="og_images/%Y/%m/",
        blank=True,
        null=True,
        help_text="Open Graph image for social sharing previews. 1200×630px recommended.",
    )
    og_image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for the OG image — used by screen readers and some social platforms.",
    )

    class Meta:
        abstract = True

    def get_seo_title(self, fallback=""):
        return self.meta_title or fallback

    def get_seo_description(self, fallback=""):
        return self.meta_description or fallback

    def get_og_image_url(self, request=None):
        """Returns absolute URL for OG image if set."""
        if self.og_image:
            if request:
                return request.build_absolute_uri(self.og_image.url)
            return self.og_image.url
        return ""
