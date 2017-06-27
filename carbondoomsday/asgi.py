"""ASGI configuration."""

from channels.asgi import get_channel_layer
from configurations import importer

importer.install()

channel_layer = get_channel_layer()
