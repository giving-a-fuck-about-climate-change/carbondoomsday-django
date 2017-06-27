"""View filters."""

import rest_framework_filters as filters

from carbondoomsday.measurements.models import CO2


class CO2Filter(filters.FilterSet):
    """CO2 view filters."""
    class Meta:
        model = CO2
        fields = {
            'ppm': '__all__',
            'date': '__all__',
        }
