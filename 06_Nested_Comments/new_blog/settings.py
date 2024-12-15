"""
Django settings for new_blog project.
"""

import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*", "database-portfolio-projects-58e826e0.koyeb.app"]
CSRF_TRUSTED_ORIGINS = ["https://database-portfolio-projects-58e826e0.koyeb.app"]

INSTALLED_FRAMEWORKS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "account",
    "core",
    "posts",
    "captcha",
    
]
INSTALLED_APPS = INSTALLED_FRAMEWORKS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'new_blog.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'new_blog.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


LOGIN_REDIRECT_URL = "/posts/"
LOGOUT_REDIRECT_URL = "/posts/"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # During development, use console backend to print emails to the console
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = env("EMAIL_HOST")
# EMAIL_PORT = env("EMAIL_PORT")
# EMAIL_STARTTLS = False
# EMAIL_USE_SSL = True
# EMAIL_USE_TLS = False
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
