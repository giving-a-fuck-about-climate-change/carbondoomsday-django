"""URL configuration."""

from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

from carbondoomsday.carbondioxide import urls

schema_view = get_swagger_view(title='CarbonDoomsDay Web API')

urlpatterns = [
    url(r"^$", schema_view),
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include(urls)),
]
