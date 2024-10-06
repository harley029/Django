from django.urls import path

from blog import views
from blog.feeds import LatestPostsFeed

app_name = "blog"


urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<int:post_id>/share/", views.PostShareView.as_view(), name="post_share"),
    path("<int:post_id>/comment/", views.PostCommentView.as_view(), name="post_comment"),
    path("tag/<slug:tag_slug>/", views.PostListView.as_view(), name="post_list_by_tag"),
    path("search/", views.PostSearchView.as_view(), name="post_search"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    # ----------------- function-based views --------------------------------
    # path("", views.post_list, name="post_list"),
    # path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post_detail"),
    # path("<int:post_id>/share/", views.post_share, name="post_share"),
    # path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    # path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    # path("feed/", LatestPostsFeed(), name="post_feed"),
    # path("search/", views.post_search, name="post_search"),
]
