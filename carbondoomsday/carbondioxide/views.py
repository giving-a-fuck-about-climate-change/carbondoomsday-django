"""Web API view sets."""

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from carbondoomsday.carbondioxide.filters import CO2MeasurementFilter
from carbondoomsday.carbondioxide.models import CO2Measurement
from carbondoomsday.carbondioxide.renderers import PaginatedCSVRenderer
from carbondoomsday.carbondioxide.serializers import CO2MeasurementSerializer


class CO2MeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    """CO2 measurements from the Mauna Loa observatory.

    This data is made available through the good work of the people at the
    Mauna Loa observatory. Their release notes say:

        These data are made freely available to the public and the scientific
        community in the belief that their wide dissemination will lead to greater
        understanding and new scientific insights.

    We currently scrape the following sources:

      * [co2_mlo_weekly.csv]
      * [co2_mlo_surface-insitu_1_ccgg_DailyData.txt]

    [co2_mlo_weekly.csv]: https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2_mlo_weekly.csv
    [co2_mlo_surface-insitu_1_ccgg_DailyData.txt]: ftp://aftp.cmdl.noaa.gov/data/trace_gases/co2/in-situ/surface/mlo/co2_mlo_surface-insitu_1_ccgg_DailyData.txt

    """ # noqa
    lookup_field = "date"
    queryset = CO2Measurement.objects.all()
    serializer_class = CO2MeasurementSerializer
    filter_class = CO2MeasurementFilter
    ordering_fields = "__all__"
    renderer_classes = (JSONRenderer, PaginatedCSVRenderer,)
