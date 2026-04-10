from django import forms
from .models import AccreditedInvestor


class AccreditedInvestorForm(forms.ModelForm):

    confirmed_accredited = forms.BooleanField(
        required=True,
        error_messages={"required": "You must confirm your accredited investor status to register."},
    )
    consent_contact = forms.BooleanField(
        required=True,
        error_messages={"required": "Please consent to being contacted to proceed."},
    )
    # Honeypot
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model  = AccreditedInvestor
        fields = [
            "first_name", "last_name", "email",
            "country", "capital_range", "referral_source",
            "confirmed_accredited", "consent_contact",
        ]
        widgets = {
            "first_name":      forms.TextInput(attrs={"placeholder": "First name",  "class": "form-control bg-black text-white border-secondary"}),
            "last_name":       forms.TextInput(attrs={"placeholder": "Last name",   "class": "form-control bg-black text-white border-secondary"}),
            "email":           forms.EmailInput(attrs={"placeholder": "your@email.com", "class": "form-control bg-black text-white border-secondary"}),
            "country":         forms.Select(attrs={"class": "form-select bg-black text-white border-secondary"}),
            "capital_range":   forms.Select(attrs={"class": "form-select bg-black text-white border-secondary"}),
            "referral_source": forms.Select(attrs={"class": "form-select bg-black text-white border-secondary"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Bot detected.")
        return cleaned
