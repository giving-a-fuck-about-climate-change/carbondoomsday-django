"""Project settings."""

import os

from configurations import Configuration, values
from dj_database_url import config as database_url_parser


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    PROJECT = "carbondoomsday"

    SCHEMA_TITLE = "CarbonDoomsDay Web API"

    DEBUG = values.BooleanValue(False)

    WSGI_APPLICATION = "carbondoomsday.wsgi.application"

    ROOT_URLCONF = "carbondoomsday.urls"

    WSGI_APPLICATION = "carbondoomsday.wsgi.application"

    DATABASES = {"default": database_url_parser()}

    SECRET_KEY = values.SecretValue()

    STATIC_URL = "/static/"
    STATIC_ROOT = "/srv/carbondoomsday/static/"

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
        "rest_framework_swagger",
        "django_filters",
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

    LOGGING = {
        "version": 1,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "carbondoomsday": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }

    CELERY_BROKER_URL = values.Value()
    CELERY_RESULT_BACKEND = values.Value()
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"

    LATEST_CO2_URL = (
        "https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2_mlo_weekly.csv"
    )

    REST_FRAMEWORK = {
        "DEFAULT_FILTER_BACKENDS": (
            "rest_framework_filters.backends.DjangoFilterBackend",
        )
    }

    SWAGGER_SETTINGS = {
        "APIS_SORTER": "alpha",
        "DOC_EXPANSION": "list",
    }


class Production(Base):
    ENVIRONMENT = "Production"


class Staging(Base):
    ENVIRONMENT = "Staging"


class Development(Base):
    ENVIRONMENT = "Development"
    DEBUG = values.BooleanValue(True)
    CELERY_TASK_ALWAYS_EAGER = values.BooleanValue(True)
