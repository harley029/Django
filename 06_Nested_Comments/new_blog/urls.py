from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls", namespace="accounts")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("captcha/", include("captcha.urls")),
    path("", RedirectView.as_view(url="/posts/", permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
