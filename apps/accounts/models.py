from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user — ready for future membership tiers."""

    class MembershipTier(models.TextChoices):
        FREE = "free", "Free"
        FOUNDING = "founding", "Founding Member ($19/mo)"
        STANDARD = "standard", "Standard ($35/mo)"
        DISCORD = "discord", "Discord Community ($49/mo)"

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    membership_tier = models.CharField(
        max_length=20,
        choices=MembershipTier.choices,
        default=MembershipTier.FREE,
    )
    membership_expires = models.DateTimeField(blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    @property
    def is_premium(self):
        from django.utils import timezone
        if self.membership_tier == self.MembershipTier.FREE:
            return False
        if self.membership_expires and self.membership_expires < timezone.now():
            return False
        return True

    @property
    def display_name(self):
        return self.get_full_name() or self.username
