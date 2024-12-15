from django.db import models
from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

User = get_user_model()


class Post(BaseModel):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["title"])]


class Comment(BaseModel):
    body = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    text_file = models.FileField(upload_to="text_files/", null=True, blank=True)
    # Для анонимных пользователей
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(validators=[EmailValidator()], null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    client_ip = models.GenericIPAddressField(null=True, blank=True)

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    def __str__(self):
        return f"{self.author or self.name} - {self.body[:50]}..."

    def get_descendants(self):
        descendants = []
        queue = [self]
        while queue:
            parent = queue.pop(0)
            children = parent.replies.all()
            descendants.extend(children)
            queue.extend(children)
        return descendants

    # class Meta:
    #     ordering = ["-created"]
