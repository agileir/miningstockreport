from decimal import Decimal

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
    jurisdiction = models.CharField(max_length=100, blank=True, help_text="Free-text jurisdiction (legacy; agent-filled). Prefer setting primary_jurisdiction FK below.")
    primary_jurisdiction = models.ForeignKey(
        "jurisdictions.Jurisdiction",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="companies",
        help_text="Primary operating jurisdiction. Pulls the risk score onto the company page.",
    )
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

    # Resources & reserves — free-form so the agent can write the technical-report
    # value verbatim, including grade and polymetallic equivalents.
    # Examples: "1.2 Moz Au @ 1.5 g/t", "10 Moz AgEq @ 120 g/t", "85 kt Cu @ 0.8%"
    resource_measured  = models.CharField(max_length=120, blank=True, help_text="Measured resource (e.g. '1.2 Moz Au @ 1.5 g/t').")
    resource_indicated = models.CharField(max_length=120, blank=True, help_text="Indicated resource.")
    resource_inferred  = models.CharField(max_length=120, blank=True, help_text="Inferred resource.")
    reserve_proven     = models.CharField(max_length=120, blank=True, help_text="Proven reserve.")
    reserve_probable   = models.CharField(max_length=120, blank=True, help_text="Probable reserve.")

    # Share structure — issued/outstanding and fully diluted snapshot at scoring date.
    # Warrants and options live on the related ShareInstrument model below.
    shares_issued_outstanding = models.PositiveBigIntegerField(null=True, blank=True, help_text="Issued and outstanding share count.")
    shares_fully_diluted      = models.PositiveBigIntegerField(null=True, blank=True, help_text="Fully diluted share count (includes warrants + options).")

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

    @property
    def cap_table_analysis(self):
        """
        Computes overhang analysis using the Treasury Stock Method (TSM):
          net new shares = ITM tranche count - (ITM proceeds / scenario price)
          dilution %     = net new shares / basic shares

        Anchors on `current_price` (the price at scoring date) so the analysis
        stays consistent with how the company looked at scoring time.

        Returns None if the scorecard lacks the basic inputs (basic shares
        and current_price). Tranches without a strike price are listed in the
        cap-table breakdown but excluded from ITM and sensitivity math.
        """
        from datetime import timedelta
        from decimal import Decimal

        basic = self.shares_issued_outstanding
        price = self.current_price
        if not basic or not price or price <= 0:
            return None

        instruments = list(self.share_instruments.all())
        warrants = [i for i in instruments if i.type == ShareInstrumentType.WARRANT]
        options  = [i for i in instruments if i.type == ShareInstrumentType.OPTION]
        # Flow-through shares are already counted in shares_issued_outstanding;
        # they don't dilute further. They DO create overhead supply at hold
        # release — surfaced separately below.
        flow_through = [i for i in instruments if i.type == ShareInstrumentType.FLOW_THROUGH]

        warrants_total = sum(w.count for w in warrants)
        options_total  = sum(o.count for o in options)
        instruments_total = warrants_total + options_total

        # TSM math runs on warrants/options only.
        priced = [i for i in instruments
                  if i.type in (ShareInstrumentType.WARRANT, ShareInstrumentType.OPTION)
                  and i.strike_price is not None]

        def _tsm(scenario_price):
            """Treasury stock method at a given price. Returns dict."""
            itm = [i for i in priced if i.strike_price < scenario_price]
            itm_count    = sum(i.count for i in itm)
            itm_proceeds = sum(Decimal(i.count) * i.strike_price for i in itm)
            buyback = (itm_proceeds / scenario_price) if scenario_price > 0 else Decimal(0)
            net_new = max(Decimal(itm_count) - buyback, Decimal(0))
            diluted = Decimal(basic) + net_new
            dilution_pct = (net_new / Decimal(basic) * Decimal(100)) if basic else Decimal(0)
            return {
                "scenario_price": scenario_price,
                "itm_count":      int(itm_count),
                "itm_proceeds":   itm_proceeds,
                "net_new_shares": int(net_new),
                "tsm_diluted":    int(diluted),
                "dilution_pct":   dilution_pct,
            }

        # Weighted-average strike, by type and overall (priced tranches only)
        def _wavg(items):
            total_count = sum(i.count for i in items)
            if not total_count:
                return None
            weighted = sum(Decimal(i.count) * i.strike_price for i in items)
            return weighted / Decimal(total_count)

        warrants_priced = [w for w in warrants if w.strike_price is not None]
        options_priced  = [o for o in options  if o.strike_price is not None]

        # Near-expiry: warrant/option tranches expiring within 12 months of the scoring date
        near_expiry_cutoff = self.scored_at.date() + timedelta(days=365)
        near_expiry = [
            i for i in instruments
            if i.type in (ShareInstrumentType.WARRANT, ShareInstrumentType.OPTION)
            and i.expiry and self.scored_at.date() <= i.expiry <= near_expiry_cutoff
        ]
        near_expiry.sort(key=lambda i: i.expiry)
        near_expiry_count = sum(i.count for i in near_expiry)

        # ── Flow-through overhead supply analysis ──
        # FT tranches are already in basic; the overhang is timing-based.
        # Tranches whose hold is releasing within 12 months of scoring create
        # potential selling pressure when the hold expires. Effective breakeven
        # (issue_price × (1 − tax_shield_pct)) is the price at which FT holders
        # are whole; trade above it implies overhead supply.
        ft_releasing = [
            i for i in flow_through
            if i.hold_release_date
            and self.scored_at.date() <= i.hold_release_date <= near_expiry_cutoff
        ]
        ft_releasing.sort(key=lambda i: i.hold_release_date)
        ft_releasing_count = sum(i.count for i in ft_releasing)
        ft_total_count = sum(i.count for i in flow_through)

        # Weighted-average breakeven across releasing tranches with known issue_price
        ft_priced = [i for i in ft_releasing if i.issue_price is not None]
        ft_breakeven_wavg = None
        ft_distance_pct = None
        if ft_priced:
            denom = sum(i.count for i in ft_priced)
            ft_breakeven_wavg = (
                sum(Decimal(i.count) * i.effective_breakeven for i in ft_priced) / Decimal(denom)
            ).quantize(Decimal("0.0001"))
            if price > 0:
                ft_distance_pct = ((price - ft_breakeven_wavg) / ft_breakeven_wavg * Decimal(100)).quantize(Decimal("0.1"))

        # Sensitivity at fixed multipliers of scoring price
        multipliers = [Decimal("0.5"), Decimal("1.0"), Decimal("1.5"), Decimal("2.0"), Decimal("3.0")]
        sensitivity = [_tsm(price * m) for m in multipliers]
        for row, m in zip(sensitivity, multipliers):
            row["multiplier"] = m

        # Headline at scoring price
        headline = _tsm(price)

        return {
            "basic":             int(basic),
            "fully_diluted":     int(self.shares_fully_diluted) if self.shares_fully_diluted else None,
            "current_price":     price,
            "warrants_total":    int(warrants_total),
            "options_total":     int(options_total),
            "instruments_total": int(instruments_total),
            "warrants_avg_strike": _wavg(warrants_priced),
            "options_avg_strike":  _wavg(options_priced),
            "all_avg_strike":      _wavg(warrants_priced + options_priced),
            "near_expiry_tranches": near_expiry,
            "near_expiry_count":    int(near_expiry_count),
            "headline":             headline,
            "sensitivity":          sensitivity,
            # Flow-through overhead-supply view
            "flow_through_total":          int(ft_total_count),
            "flow_through_releasing":      ft_releasing,
            "flow_through_releasing_count": int(ft_releasing_count),
            "flow_through_breakeven_wavg":  ft_breakeven_wavg,
            "flow_through_distance_pct":    ft_distance_pct,
            "flow_through_tax_shield_pct":  FLOW_THROUGH_TAX_SHIELD_PCT,
        }


class ShareInstrumentType(models.TextChoices):
    WARRANT      = "warrant",      "Warrant"
    OPTION       = "option",       "Option"
    FLOW_THROUGH = "flow_through", "Flow-through"


# Default tax-shield assumption used to compute effective breakeven on
# flow-through shares. Roughly the top-bracket Canadian effective rate
# (federal + provincial + super-FT enhancements). Override at display
# time if a per-jurisdiction model is added later.
FLOW_THROUGH_TAX_SHIELD_PCT = Decimal("0.50")


class ShareInstrument(models.Model):
    """
    A tranche of warrants, options, or flow-through shares associated with a
    scorecard. Multiple rows per scorecard — one per strike/expiry (warrants/
    options) or per issue-price/hold-release (flow-through).
    """
    scorecard = models.ForeignKey(
        VerdictScorecard, on_delete=models.CASCADE, related_name="share_instruments",
    )
    type = models.CharField(max_length=20, choices=ShareInstrumentType.choices)
    count = models.PositiveBigIntegerField(help_text="Number of warrants, options, or flow-through shares in this tranche.")
    # Used by warrant/option tranches.
    strike_price = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True,
        help_text="Strike price (warrants/options). Leave blank if unknown.",
    )
    expiry = models.DateField(null=True, blank=True, help_text="Expiry date (warrants/options). Leave blank if unknown.")
    # Used by flow-through tranches.
    issue_price = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True,
        help_text="Issue price (flow-through tranches). The headline placement price.",
    )
    hold_release_date = models.DateField(
        null=True, blank=True,
        help_text="Date the 4-month flow-through hold expires and shares free-trade.",
    )
    notes = models.CharField(
        max_length=120, blank=True,
        help_text="Optional label, e.g. 'Tranche A', 'Director options', 'Critical-minerals super-FT'.",
    )

    class Meta:
        ordering = ["type", "strike_price", "issue_price", "expiry", "hold_release_date"]

    def __str__(self):
        bits = [self.get_type_display(), f"{self.count:,}"]
        if self.strike_price is not None:
            bits.append(f"@ {self.strike_price}")
        if self.issue_price is not None:
            bits.append(f"FT@ {self.issue_price}")
        if self.expiry:
            bits.append(self.expiry.isoformat())
        if self.hold_release_date:
            bits.append(f"release {self.hold_release_date.isoformat()}")
        return " ".join(bits)

    @property
    def effective_breakeven(self):
        """
        For flow-through tranches: the price at which an FT investor in the
        top tax bracket recovers their after-tax cost. Above this price,
        FT holders are profitable and create overhead supply at hold release.
        Returns None for non-FT instruments or when issue_price is unknown.
        """
        if self.type != ShareInstrumentType.FLOW_THROUGH or self.issue_price is None:
            return None
        return (self.issue_price * (Decimal("1") - FLOW_THROUGH_TAX_SHIELD_PCT)).quantize(Decimal("0.0001"))


class CompanyQueueStatus(models.TextChoices):
    PENDING       = "pending",       "Pending verification"
    ACTIVE        = "active",        "Active — ready to promote"
    PROMOTED      = "promoted",      "Promoted to Company"
    DELISTED      = "delisted",      "Delisted"
    ACQUIRED      = "acquired",      "Acquired"
    OUT_OF_SCOPE  = "out_of_scope",  "Out of scope (exchange)"
    REJECTED      = "rejected",      "Rejected"


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


class ShellCandidateStatus(models.TextChoices):
    DORMANT       = "dormant",       "Dormant (no recent volume)"
    WATCHING      = "watching",      "Watching (actively evaluating)"
    RTO_COMPLETED = "rto_completed", "RTO completed (became another company)"
    BACK_ACTIVE   = "back_active",   "Resumed trading"
    DELISTED      = "delisted",      "Delisted from exchange"
    REJECTED      = "rejected",      "Not suitable for RTO"


class ShellCandidate(models.Model):
    """
    Mining-sector shells — companies still listed on an exchange but with
    effectively no trading volume. Tracked separately from CompanyQueue
    because shells are a sourcing/intelligence asset, not coverage candidates.

    The lifecycle here differs from the active research pipeline: a shell
    can stay dormant for years, eventually get RTO'd into a new entity, get
    delisted, or quietly resume trading. None of those paths involve our
    Verdict Framework or scorecard process.
    """
    ticker = models.CharField(max_length=20)
    exchange = models.CharField(max_length=10, choices=Exchange.choices)
    name = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True, default="Canada")

    status = models.CharField(
        max_length=20,
        choices=ShellCandidateStatus.choices,
        default=ShellCandidateStatus.DORMANT,
        db_index=True,
    )

    # Volume / price snapshot at time of last verification
    last_known_price = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True,
        help_text="Last close price (CAD) at time of last verification.",
    )
    avg_dollar_volume_5d = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
        help_text="5-day avg dollar volume at time of last verification.",
    )
    avg_share_volume_5d = models.PositiveBigIntegerField(
        null=True, blank=True,
        help_text="5-day avg share volume at time of last verification.",
    )
    market_cap_cad = models.BigIntegerField(
        null=True, blank=True,
        help_text="Market cap in CAD at time of last verification.",
    )

    # Listing
    listing_date = models.DateField(
        null=True, blank=True,
        help_text="When the shell first started trading on its exchange.",
    )

    # Provenance
    source = models.CharField(
        max_length=120, blank=True,
        help_text="Where this shell was identified (scan source + date).",
    )
    notes = models.TextField(blank=True)

    # Lifecycle outcomes
    rto_target_name = models.CharField(
        max_length=200, blank=True,
        help_text="If RTO completed: the resulting company name.",
    )
    verified_at = models.DateTimeField(
        null=True, blank=True,
        help_text="When the volume/price snapshot above was last refreshed.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shell candidate"
        verbose_name_plural = "Shell candidates"
        ordering = ["status", "exchange", "ticker"]
        unique_together = ("ticker", "exchange")
        indexes = [
            models.Index(fields=["status", "exchange"]),
        ]

    def __str__(self):
        return f"{self.exchange}:{self.ticker} — {self.name} ({self.get_status_display()})"
