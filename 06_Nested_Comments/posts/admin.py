from django.contrib import admin
from posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "body", "author"]
    list_filter = ["created", "author"]
    search_fields = ["title", "author"]
    ordering = ["created"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "body",
        "name",
        "email",
        "author",
        "post",
        "parent",
        "client_ip",
        "image",
        "text_file",
        "website",
        "created",
    ]
    list_filter = ["created", "updated"]
    search_fields = ["name", "email", "author", "body"]
    ordering = ["created"]
