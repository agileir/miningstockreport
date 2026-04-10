from django.urls import path
from . import views

app_name = "verdict"

urlpatterns = [
    path("",                            views.CompanyListView.as_view(),    name="company_list"),
    path("<slug:slug>/",                views.CompanyDetailView.as_view(),  name="company_detail"),
    path("<slug:slug>/scorecard/<int:pk>/", views.ScorecardDetailView.as_view(), name="scorecard_detail"),
]
