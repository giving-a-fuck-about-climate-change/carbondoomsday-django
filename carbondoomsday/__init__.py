"""Project package."""

from configurations import importer

importer.install()

from carbondoomsday.celeryconf import app as celery_app

__all__ = ['celery_app']
