"""Channel consumers."""

import logging

from channels.generic.websockets import JsonWebsocketConsumer

from carbondoomsday.carbondioxide.models import CO2Measurement

logger = logging.getLogger(__name__)


class CO2FrontEndConsumer(JsonWebsocketConsumer):
    """Channel consumer for front-end CO2 related communication."""
    def connection_groups(self, **kwargs):
        return ["co2"]

    def receive(self, filters, **kwargs):
        msg = "Here are the filters I got from the front-end: {}"
        logger.info(msg.format(filters))

        filtered = CO2Measurement.objects.filter(**filters)
        json_payload = [obj.tojson() for obj in filtered]

        msg = "Here is what I am sending back: {}"
        logger.info(msg.format(json_payload))

        self.send(json_payload)
