from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("", views.SubscribeView.as_view(), name="subscribe"),
    path("download/<int:pk>/", views.LeadMagnetDownloadView.as_view(), name="download"),
]
