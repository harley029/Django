from django.urls import path, include
from django.contrib.auth import views as auth_views

from account.views import RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    ]