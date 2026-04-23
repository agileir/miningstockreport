from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("about/author/<str:username>/", views.author_profile, name="author_profile"),
    path("about/methodology/", views.methodology, name="methodology"),
    path("about/disclaimer/", views.disclaimer, name="disclaimer"),
    path("tools/", views.tools_index, name="tools_index"),
    path("tools/nav-calculator/", views.nav_calculator, name="nav_calculator"),
    path("tools/copper-nav-calculator/", views.nav_calculator_copper, name="nav_calculator_copper"),
    path("tools/silver-nav-calculator/", views.nav_calculator_silver, name="nav_calculator_silver"),
    path("tools/polymetallic-nav-calculator/", views.nav_calculator_polymetallic, name="nav_calculator_polymetallic"),
]
