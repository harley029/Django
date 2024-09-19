from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

from core.models import BaseModel


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.STATUS["PB"])


class Post(BaseModel):
    STATUS = {"DR": "Draft", "PB": "Published"}

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=STATUS.items(), default="DR")

    objects = models.Manager()  # менеджер, застосовуваний за замовчуванням
    published = PublishedManager()  # конкретно-прикладний менеджер
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [models.Index(fields=["-publish"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [ models.Index(fields=['created_at']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
