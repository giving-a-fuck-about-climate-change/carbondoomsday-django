"""Model layer serializers."""

from rest_framework import serializers

from carbondoomsday.measurements.models import CO2


class CO2Serializer(serializers.ModelSerializer):
    """CO2 model serializer."""
    class Meta:
        model = CO2
        fields = ('ppm', 'date')
