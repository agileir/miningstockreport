from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField
from apps.core.seo import SEOMixin


class Exchange(models.TextChoices):
    TSXV = "TSXV", "TSX Venture (TSXV)"
    TSX = "TSX", "Toronto Stock Exchange (TSX)"
    CSE = "CSE", "Canadian Securities Exchange (CSE)"
    ASX = "ASX", "Australian Securities Exchange (ASX)"
    OTC = "OTC", "OTC Markets"
    NYSE = "NYSE", "NYSE / NYSE American"
    LSE = "LSE", "London Stock Exchange (LSE)"
    OTHER = "OTHER", "Other"


class VerdictChoice(models.TextChoices):
    BUY = "BUY", "Buy"
    WATCH = "WATCH", "Watch"
    AVOID = "AVOID", "Avoid"


class CompanyTier(models.TextChoices):
    JUNIOR = "junior", "Junior / Explorer"
    MID    = "mid",    "Mid-Tier Producer"
    MAJOR  = "major",  "Major Producer"


class Company(SEOMixin, models.Model):
    """A mining company that can be analysed via the Verdict Framework."""
    name = models.CharField(max_length=200, blank=True, help_text="Leave blank — AI agent will fill this in from the ticker.")
    slug = AutoSlugField(populate_from="name", unique=True, always_update=False)
    ticker = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10, choices=Exchange.choices)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="companies/logos/", blank=True, null=True)

    # Key facts (updated manually or via future data feed)
    market_cap_cad = models.BigIntegerField(
        null=True, blank=True, help_text="Market cap in CAD cents to avoid float issues."
    )
    jurisdiction = models.CharField(max_length=100, blank=True, help_text="e.g. British Columbia, Nevada, Peru")
    primary_commodity = models.CharField(max_length=50, blank=True, help_text="e.g. Gold, Copper, Silver")
    tier = models.CharField(
        max_length=10, choices=CompanyTier.choices, default=CompanyTier.JUNIOR,
        help_text="Controls page layout. Juniors show Verdict Framework. Majors/mid-tiers show producer profile.",
    )
    needs_research = models.BooleanField(
        default=False,
        help_text="Flag for the AI agent to research and generate a verdict scorecard.",
    )
    data_filled = models.BooleanField(
        default=False,
        help_text="Set automatically when the AI agent fills in company details from the ticker.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        import re
        from django.utils.text import slugify
        self.ticker = self.ticker.upper()
        # Regenerate slug if it's still a fallback like "company-16"
        if self.name and re.match(r"^company-\d+$", self.slug or ""):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticker} — {self.name}"

    def get_absolute_url(self):
        return reverse("verdict:company_detail", kwargs={"slug": self.slug})

    @property
    def latest_verdict(self):
        return self.scorecards.order_by("-scored_at").first()


class VerdictScorecard(SEOMixin, models.Model):
    """
    The 5-factor Verdict Framework scorecard.
    Each factor scored 1–5. Composite score drives BUY / WATCH / AVOID.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="scorecards")

    # Factor 1 — Management skin-in-the-game
    management_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 = No insider ownership / red flags. 5 = Significant aligned ownership.",
    )
    management_notes = models.TextField(blank=True)

    # Factor 2 — Project geology quality
    geology_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 = Inferred only / poor grade. 5 = Measured+Indicated with strong grade/scale.",
    )
    geology_notes = models.TextField(blank=True)

    # Factor 3 — Capital structure health
    capital_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 = Highly diluted / warrant overhang. 5 = Clean structure, funded.",
    )
    capital_notes = models.TextField(blank=True)

    # Factor 4 — Catalyst proximity
    catalyst_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 = No near-term catalysts. 5 = Drill results / feasibility imminent.",
    )
    catalyst_notes = models.TextField(blank=True)

    # Factor 5 — Comparable acquisition value
    acquisition_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 = Trading at/above peer acquisition multiples. 5 = Deep discount to peers.",
    )
    acquisition_notes = models.TextField(blank=True)

    # Output
    verdict = models.CharField(max_length=5, choices=VerdictChoice.choices)
    analyst_summary = models.TextField(help_text="Plain-language summary published with the scorecard.")

    # P/NAV calculation fields (from the technical report video framework)
    nav_per_share = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    p_nav_multiple = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    is_published = models.BooleanField(default=False)
    scored_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scored_at"]

    def __str__(self):
        return f"{self.company.ticker} — {self.verdict} ({self.scored_at.date()})"

    def get_absolute_url(self):
        return reverse(
            "verdict:scorecard_detail",
            kwargs={
                "slug": self.company.slug,
                "date": self.scored_at.strftime("%Y-%m-%d"),
            },
        )

    @property
    def composite_score(self):
        return (
            self.management_score
            + self.geology_score
            + self.capital_score
            + self.catalyst_score
            + self.acquisition_score
        )

    @property
    def composite_score_pct(self):
        """Returns score as percentage of maximum (25)."""
        return round((self.composite_score / 25) * 100)

    def save(self, *args, **kwargs):
        """Auto-calculate P/NAV multiple if both fields are set."""
        if self.nav_per_share and self.current_price and self.nav_per_share > 0:
            self.p_nav_multiple = self.current_price / self.nav_per_share
        super().save(*args, **kwargs)


class CompanyQueueStatus(models.TextChoices):
    PENDING         = "pending",         "Pending verification"
    ACTIVE          = "active",          "Active — ready to promote"
    PROMOTED        = "promoted",        "Promoted to Company"
    SHELL_CANDIDATE = "shell_candidate", "Shell candidate (dormant; potential RTO)"
    DELISTED        = "delisted",        "Delisted"
    ACQUIRED        = "acquired",        "Acquired"
    OUT_OF_SCOPE    = "out_of_scope",    "Out of scope (exchange)"
    REJECTED        = "rejected",        "Rejected"


class CompanyQueue(models.Model):
    """
    Candidate ticker queue. Tickers sourced from third-party directories
    (miningfeeds.com, SEDI search, editorial suggestion) land here before
    they become Company records. The promote_queue management command
    creates Company records from ACTIVE queue entries at a controlled
    pace; the data-fill and research agents take it from there.
    """
    ticker = models.CharField(max_length=20)
    exchange = models.CharField(max_length=10, choices=Exchange.choices)
    name = models.CharField(max_length=200, blank=True)
    primary_commodity = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True, help_text="Country of primary operations")
    status = models.CharField(
        max_length=20, choices=CompanyQueueStatus.choices,
        default=CompanyQueueStatus.PENDING, db_index=True,
    )
    source = models.CharField(
        max_length=100, blank=True,
        help_text="Where this ticker was sourced from (e.g. 'miningfeeds.com/gold').",
    )
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="queue_entries",
        help_text="Set when this queue entry is promoted to a Company record.",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company queue entry"
        verbose_name_plural = "Company queue"
        ordering = ["status", "ticker"]
        unique_together = ("ticker", "exchange")
        indexes = [
            models.Index(fields=["status", "exchange"]),
        ]

    def __str__(self):
        return f"{self.exchange}:{self.ticker} ({self.get_status_display()})"
