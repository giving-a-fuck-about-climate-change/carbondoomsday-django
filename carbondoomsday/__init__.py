"""Project package."""

from configurations import importer
from .celery import app as celery_app  # noqa


importer.install()
