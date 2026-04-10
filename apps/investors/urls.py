from django.urls import path
from . import views

app_name = "investors"

urlpatterns = [
    path("",         views.AccreditedInvestorRegisterView.as_view(), name="register"),
    path("thank-you/", views.AccreditedInvestorThankYouView.as_view(), name="thank_you"),
]
