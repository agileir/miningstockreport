from django.urls import path
from . import views

app_name = "videos"

urlpatterns = [
    path("", views.VideoListView.as_view(), name="video_list"),
    path("pillar/<str:pillar>/", views.VideoListView.as_view(), name="video_list_by_pillar"),
    path("<slug:slug>/", views.VideoDetailView.as_view(), name="video_detail"),
]
