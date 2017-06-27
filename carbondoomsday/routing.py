"""Channels routing."""

from channels.routing import route_class

from carbondoomsday.carbondioxide.consumers import CO2FrontEndConsumer

appchannels = [
    route_class(CO2FrontEndConsumer,  path=r"^/co2/"),
]
