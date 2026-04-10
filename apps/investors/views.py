from django.views.generic import FormView, TemplateView
from django.http import JsonResponse
from django.contrib import messages
from .forms import AccreditedInvestorForm
from .models import AccreditedInvestor


class AccreditedInvestorRegisterView(FormView):
    template_name = "investors/register.html"
    form_class    = AccreditedInvestorForm
    success_url   = "/investors/thank-you/"

    def form_valid(self, form):
        investor = form.save(commit=False)
        # Capture IP for consent record
        x_forwarded = self.request.META.get("HTTP_X_FORWARDED_FOR")
        investor.consent_ip = (
            x_forwarded.split(",")[0].strip() if x_forwarded
            else self.request.META.get("REMOTE_ADDR")
        )
        investor.save()

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "ok"})

        messages.success(
            self.request,
            "Registration received. We'll review your profile and be in touch within 5 business days.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
        return super().form_invalid(form)


class AccreditedInvestorThankYouView(TemplateView):
    template_name = "investors/thank_you.html"
