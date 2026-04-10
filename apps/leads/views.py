from django.views.generic import FormView
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Subscriber, LeadMagnet
from .forms import SubscribeForm


class SubscribeView(FormView):
    template_name = "leads/subscribe.html"
    form_class = SubscribeForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        first_name = form.cleaned_data.get("first_name", "")
        source = form.cleaned_data.get("source", Subscriber.Source.HOMEPAGE)
        lead_magnet_id = form.cleaned_data.get("lead_magnet_id")

        lead_magnet = None
        if lead_magnet_id:
            lead_magnet = LeadMagnet.objects.filter(pk=lead_magnet_id, is_active=True).first()

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "source": source,
                "lead_magnet": lead_magnet,
            },
        )

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "status": "ok",
                "created": created,
                "download_url": lead_magnet.file.url if lead_magnet else None,
            })

        messages.success(
            self.request,
            "You're in! Check your inbox — your download link is on its way."
            if lead_magnet else
            "You're subscribed. We'll be in touch when new analysis drops.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", "/")

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
        return super().form_invalid(form)


class LeadMagnetDownloadView(View):
    """Serve lead magnet file — gated behind confirmed subscription."""

    def get(self, request, pk):
        magnet = get_object_or_404(LeadMagnet, pk=pk, is_active=True)
        email = request.GET.get("email", "")
        if not Subscriber.objects.filter(email=email, is_active=True).exists():
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Subscribe first to access this download.")
        return FileResponse(magnet.file.open("rb"), as_attachment=True, filename=magnet.file.name.split("/")[-1])
