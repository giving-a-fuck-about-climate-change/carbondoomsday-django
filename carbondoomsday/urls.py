"""URL configuration."""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

from carbondoomsday.carbondioxide import urls
from carbondoomsday.carbondioxide.templates import CO2TrackerView

schema_view = get_swagger_view(title=settings.SCHEMA_TITLE)

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^apidocs/", schema_view),
    url(r"^api/", include(urls)),
    url(r"^$", CO2TrackerView.as_view(), name="co2-tracker"),
]
