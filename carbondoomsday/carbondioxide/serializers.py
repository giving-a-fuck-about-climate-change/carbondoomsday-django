"""Model layer serializers."""

from rest_framework import serializers

from carbondoomsday.carbondioxide.models import CO2Measurement


class CO2MeasurementSerializer(serializers.ModelSerializer):
    """CO2 measurement model serializer."""
    class Meta:
        model = CO2Measurement
        fields = ("ppm", "date")
