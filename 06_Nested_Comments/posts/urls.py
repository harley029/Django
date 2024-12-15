from django.urls import path
from posts import views


app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("add_post/", views.AddPostView.as_view(), name="add_post"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<int:post_id>/add_comment/", views.AddCommentView.as_view(), name="post_comment"),
    path("<int:pk>/comment/<int:parent_comment_id>/reply/", views.ReplyCommentView.as_view(), name="comment_reply",),
    path("comment/<int:comment_id>/text_file/", views.TextFileView.as_view(), name="text_file_view"),
    path("<int:post_id>/comment/<int:comment_id>/", views.CommentDetailView.as_view(), name="comment_detail"),
]
