from django.urls import path
from . import views

app_name = "verdict"

urlpatterns = [
    path("",                            views.CompanyListView.as_view(),    name="company_list"),
    path("<slug:slug>/",                views.CompanyDetailView.as_view(),  name="company_detail"),
    path("<slug:slug>/scorecard/<str:date>/", views.ScorecardDetailView.as_view(), name="scorecard_detail"),
    # 301 redirect from old pk-based URLs
    path("<slug:slug>/scorecard/<int:pk>/", views.scorecard_pk_redirect, name="scorecard_detail_legacy"),
]
