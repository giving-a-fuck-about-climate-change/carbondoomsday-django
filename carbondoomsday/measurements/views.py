"""Web API view sets."""

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from carbondoomsday.measurements.filters import CO2Filter
from carbondoomsday.measurements.models import CO2
from carbondoomsday.measurements.renderers import PaginatedCSVRenderer
from carbondoomsday.measurements.serializers import CO2Serializer


class CO2ViewSet(viewsets.ReadOnlyModelViewSet):
    """CO2 measurements from the Mauna Loa observatory.

    This data is made available through the good work of the people at the
    Mauna Loa observatory. Their release notes say:

        These data are made freely available to the public and the scientific
        community in the belief that their wide dissemination will lead to greater
        understanding and new scientific insights.

    We currently scrape the following sources:

      * [co2_mlo_weekly.csv]
      * [co2_mlo_surface-insitu_1_ccgg_DailyData.txt]
      * [weekly_mlo.csv]

    We have daily CO2 measurements as far back as 1958.

    Learn about using pagination via [the 3rd party documentation].

    [co2_mlo_weekly.csv]: https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2_mlo_weekly.csv
    [co2_mlo_surface-insitu_1_ccgg_DailyData.txt]: ftp://aftp.cmdl.noaa.gov/data/trace_gases/co2/in-situ/surface/mlo/co2_mlo_surface-insitu_1_ccgg_DailyData.txt
    [weekly_mlo.csv]: http://scrippsco2.ucsd.edu/sites/default/files/data/in_situ_co2/weekly_mlo.csv
    [the 3rd party documentation]: http://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination

    """ # noqa
    lookup_field = 'date'
    queryset = CO2.objects.all()
    serializer_class = CO2Serializer
    filter_class = CO2Filter
    ordering_fields = '__all__'
    ordering = ('-date',)
    renderer_classes = (JSONRenderer, PaginatedCSVRenderer,)
