from django import forms
from .models import Subscriber


class SubscribeForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "your@email.com", "class": "form-control"})
    )
    first_name = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "First name (optional)", "class": "form-control"}),
    )
    source = forms.ChoiceField(
        choices=Subscriber.Source.choices,
        widget=forms.HiddenInput(),
        required=False,
    )
    lead_magnet_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    # Honeypot field — if filled, it's a bot
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Bot detected.")
        return cleaned
