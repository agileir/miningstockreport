from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField
from apps.core.seo import SEOMixin


class RegionType(models.TextChoices):
    COUNTRY   = "country",   "Country"
    PROVINCE  = "province",  "Province"
    STATE     = "state",     "State"
    TERRITORY = "territory", "Territory"
    REGION    = "region",    "Region"


class RiskLabel(models.TextChoices):
    LOW      = "LOW",      "Low Risk"
    MODERATE = "MODERATE", "Moderate Risk"
    ELEVATED = "ELEVATED", "Elevated Risk"
    HIGH     = "HIGH",     "High Risk"
    EXTREME  = "EXTREME",  "Extreme Risk"


class Jurisdiction(SEOMixin, models.Model):
    """
    A mining jurisdiction — country or sub-national region. Scored on 5
    factors (1–5 each). Composite 5–25 — higher means LESS risk.
    """
    name = models.CharField(max_length=120, help_text="e.g. 'British Columbia', 'Nevada', 'Peru'")
    slug = AutoSlugField(populate_from="name", unique=True, always_update=False)
    country = models.CharField(max_length=80, help_text="Parent country, e.g. 'Canada'. For country-level rows, repeat the name here.")
    country_code = models.CharField(max_length=2, blank=True, help_text="ISO 3166-1 alpha-2, e.g. 'CA', 'US', 'AU'.")
    region_type = models.CharField(
        max_length=12, choices=RegionType.choices, default=RegionType.COUNTRY,
    )

    # Five sub-scores. 1 = worst (most risk), 5 = best (least risk).
    permitting_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Permitting timeline & predictability. 1 = years of delay / unpredictable. 5 = clear, fast, predictable.",
    )
    permitting_notes = models.TextField(blank=True, help_text="One-sentence justification.")

    fiscal_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Fiscal regime stability — royalties, tax, no surprise changes. 1 = recent hostile changes. 5 = stable for decades.",
    )
    fiscal_notes = models.TextField(blank=True)

    political_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Political & security risk. 1 = active conflict / expropriation risk. 5 = stable democracy, rule of law.",
    )
    political_notes = models.TextField(blank=True)

    infrastructure_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Infrastructure & power. 1 = remote, no roads/grid. 5 = full road, rail, power access.",
    )
    infrastructure_notes = models.TextField(blank=True)

    community_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Indigenous, community, ESG complexity. 1 = blocked / litigation. 5 = strong community support, clear consultation framework.",
    )
    community_notes = models.TextField(blank=True)

    # Narrative
    summary = models.TextField(
        help_text="2–4 paragraph plain-language summary of why this jurisdiction earned its scores.",
    )
    whats_changed = models.TextField(
        blank=True,
        help_text="Optional 'what changed recently' note — new legislation, election outcomes, recent permits granted/denied.",
    )

    last_assessed_at = models.DateField(
        null=True, blank=True,
        help_text="Date this assessment was last reviewed. Update annually after Fraser Institute releases.",
    )
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["country", "name"]
        constraints = [
            models.UniqueConstraint(fields=["country", "name"], name="uniq_country_name"),
        ]

    def __str__(self):
        if self.region_type == RegionType.COUNTRY:
            return self.name
        return f"{self.name}, {self.country}"

    def get_absolute_url(self):
        return reverse("jurisdictions:detail", kwargs={"slug": self.slug})

    @property
    def composite_score(self):
        return (
            self.permitting_score
            + self.fiscal_score
            + self.political_score
            + self.infrastructure_score
            + self.community_score
        )

    @property
    def composite_score_pct(self):
        return round((self.composite_score / 25) * 100)

    @property
    def risk_label(self):
        s = self.composite_score
        if s >= 22: return RiskLabel.LOW
        if s >= 18: return RiskLabel.MODERATE
        if s >= 13: return RiskLabel.ELEVATED
        if s >= 8:  return RiskLabel.HIGH
        return RiskLabel.EXTREME

    @property
    def risk_label_display(self):
        return RiskLabel(self.risk_label).label

    @property
    def risk_badge_class(self):
        """Bootstrap badge class for the risk level."""
        return {
            RiskLabel.LOW:      "bg-success",
            RiskLabel.MODERATE: "bg-info text-dark",
            RiskLabel.ELEVATED: "bg-warning text-dark",
            RiskLabel.HIGH:     "bg-danger",
            RiskLabel.EXTREME:  "bg-dark border border-danger text-danger",
        }[self.risk_label]

    @property
    def factors(self):
        """Iterable of factor dicts for templates."""
        return [
            {"label": "Permitting Timeline & Predictability", "score": self.permitting_score,     "notes": self.permitting_notes,     "key": "permitting"},
            {"label": "Fiscal Regime Stability",              "score": self.fiscal_score,         "notes": self.fiscal_notes,         "key": "fiscal"},
            {"label": "Political & Security Risk",            "score": self.political_score,      "notes": self.political_notes,      "key": "political"},
            {"label": "Infrastructure & Power",               "score": self.infrastructure_score, "notes": self.infrastructure_notes, "key": "infrastructure"},
            {"label": "Indigenous, Community & ESG",          "score": self.community_score,      "notes": self.community_notes,      "key": "community"},
        ]
