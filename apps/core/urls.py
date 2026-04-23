from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("about/author/<str:username>/", views.author_profile, name="author_profile"),
    path("about/methodology/", views.methodology, name="methodology"),
    path("about/disclaimer/", views.disclaimer, name="disclaimer"),
    path("tools/nav-calculator/", views.nav_calculator, name="nav_calculator"),
]
