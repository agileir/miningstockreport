from django.urls import path
from . import views

app_name = "jurisdictions"

urlpatterns = [
    path("",              views.JurisdictionListView.as_view(),   name="index"),
    path("<slug:slug>/",  views.JurisdictionDetailView.as_view(), name="detail"),
]
