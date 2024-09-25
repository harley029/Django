from .base import *

DEBUG = False

ADMINS = [
    ("Oleksandr, Kh.", "harley029@gmail.com"),
]
ALLOWED_HOSTS = ["educaproject.com", "www.educaproject.com"]

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": "db",
        "PORT": env("DATABASE_PORT"),
    }
}

REDIS_URL = "redis://cache:6379"
CACHES["default"]["LOCATION"] = REDIS_URL
CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [REDIS_URL]
