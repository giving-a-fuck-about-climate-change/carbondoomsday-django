"""Project package."""

from configurations import importer

from .celeryconf import app as celery_app

importer.install()

__all__ = ['celery_app']
