"""URL configuration."""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

from carbondoomsday.measurements import urls

schema_view = get_swagger_view(title=settings.SCHEMA_TITLE)

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^apidocs/", schema_view),
    url(r"^api/", include(urls))
]
