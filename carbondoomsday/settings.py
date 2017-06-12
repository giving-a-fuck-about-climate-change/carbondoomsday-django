"""Project settings."""

import logging
import os

from configurations import Configuration, values
from dj_database_url import config as database_url_parser

logger = logging.getLogger(__name__)


class Base(Configuration):
    DEBUG = values.BooleanValue(False)
    INSTALLED_APPS = (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "carbondoomsday.carbondioxide",
        "rest_framework",
        "django_extensions",
    )
    MIDDLEWARE_CLASSES = (
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    )
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    WSGI_APPLICATION = "carbondoomsday.wsgi.application"
    ROOT_URLCONF = "carbondoomsday.urls"
    WSGI_APPLICATION = "carbondoomsday.wsgi.application"
    DATABASES = {"default": database_url_parser()}
    SECRET_KEY = values.SecretValue()
    STATIC_URL = "/static/"


class Production(Base):
    ENVIRONMENT = "Production"


class Staging(Base):
    ENVIRONMENT = "Staging"


class Development(Base):
    ENVIRONMENT = "Development"
    DEBUG = values.BooleanValue(True)
