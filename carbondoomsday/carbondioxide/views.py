"""Web API view sets."""

from rest_framework import viewsets

from carbondoomsday.carbondioxide.filters import CO2MeasurementFilter
from carbondoomsday.carbondioxide.models import CO2Measurement
from carbondoomsday.carbondioxide.serializers import CO2MeasurementSerializer


class CO2MeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    """CO2 measurements view set."""
    lookup_field = "date"
    queryset = CO2Measurement.objects.all()
    serializer_class = CO2MeasurementSerializer
    filter_class = CO2MeasurementFilter
