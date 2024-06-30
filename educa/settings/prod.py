from decouple import config
from .base import *

DEBUG = False
ADMINS = [
    ("Omar Raafat", "omar.raafat@mydomain.com"),
]
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}
