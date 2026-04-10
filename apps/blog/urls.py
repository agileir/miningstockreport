from django.urls import path
from . import views

app_name = "blog"

# /analysis/ is a stronger topical signal than /blog/
# Set this before any content is indexed — changing later is costly
urlpatterns = [
    path("",                        views.PostListView.as_view(),             name="post_list"),
    path("pillar/<str:pillar>/",    views.PostListView.as_view(),             name="post_list_by_pillar"),
    path("<slug:slug>/",            views.PostDetailView.as_view(),           name="post_detail"),
]
