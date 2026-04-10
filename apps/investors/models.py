from django.db import models


class AccreditedInvestor(models.Model):

    class Country(models.TextChoices):
        CANADA  = "CA", "Canada"
        AUSTRALIA = "AU", "Australia"
        UK      = "UK", "United Kingdom"
        USA     = "US", "United States"
        OTHER   = "OTHER", "Other"

    class CapitalRange(models.TextChoices):
        TIER_1 = "50k-150k",   "$50K – $150K"
        TIER_2 = "150k-500k",  "$150K – $500K"
        TIER_3 = "500k-1m",    "$500K – $1M"
        TIER_4 = "1m+",        "$1M+"

    class ReferralSource(models.TextChoices):
        YOUTUBE   = "youtube",   "YouTube"
        NEWSLETTER = "newsletter","Newsletter referral"
        SEARCH    = "search",    "Search / Google"
        SOCIAL    = "social",    "Social media"
        WORD_OF_MOUTH = "wom",   "Word of mouth"
        OTHER     = "other",     "Other"

    class Status(models.TextChoices):
        PENDING   = "pending",   "Pending review"
        APPROVED  = "approved",  "Approved"
        CONTACTED = "contacted", "Contacted"
        DECLINED  = "declined",  "Declined"
        INACTIVE  = "inactive",  "Inactive"

    # Personal details
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    country    = models.CharField(max_length=10, choices=Country.choices)
    capital_range = models.CharField(max_length=20, choices=CapitalRange.choices)
    referral_source = models.CharField(max_length=20, choices=ReferralSource.choices, blank=True)

    # Consent — stored explicitly for regulatory purposes
    confirmed_accredited = models.BooleanField(
        default=False,
        help_text="Investor confirmed accredited status at time of registration.",
    )
    consent_contact = models.BooleanField(
        default=False,
        help_text="Investor consented to be contacted about deal flow.",
    )
    consent_timestamp = models.DateTimeField(auto_now_add=True)
    consent_ip = models.GenericIPAddressField(
        null=True, blank=True,
        help_text="IP address at time of consent — retained for compliance.",
    )

    # CRM fields (manual, until CRM integration is built)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    internal_notes = models.TextField(blank=True, help_text="Private notes — not visible to investor.")
    assigned_to    = models.CharField(max_length=100, blank=True, help_text="Team member handling this lead.")
    last_contacted = models.DateTimeField(null=True, blank=True)

    registered_at  = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-registered_at"]
        verbose_name = "Accredited Investor"
        verbose_name_plural = "Accredited Investors"

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
