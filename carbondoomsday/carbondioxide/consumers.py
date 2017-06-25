"""Channel consumers."""

import logging

from channels.generic.websockets import JsonWebsocketConsumer

logger = logging.getLogger(__name__)


class FrontEndConsumer(JsonWebsocketConsumer):
    """Channel consumer for front-end/back-end communication."""
    http_user = True

    def connection_groups(self, **kwargs):
        return ["frontend"]

    def connect(self, message, **kwargs):
        logger.debug("Connected over the channel bro.")

    def receive(self, content, **kwargs):
        logger.debug("Received a message over the channel bro.")

    def disconnect(self, message, **kwargs):
        pass
