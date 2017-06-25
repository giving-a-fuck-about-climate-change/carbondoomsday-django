"""Channels routing."""

from channels.routing import route_class

from carbondoomsday.carbondioxide.consumers import FrontEndConsumer

channel_routing = [
    route_class(FrontEndConsumer,  path=r"^/frontend/"),
]
