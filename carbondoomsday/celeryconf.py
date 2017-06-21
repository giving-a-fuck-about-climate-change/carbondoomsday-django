"""Celery configuration module."""

from celery import Celery
from django.conf import settings


app = Celery(settings.PROJECT)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
