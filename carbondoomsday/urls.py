"""URL configuration."""

from django.conf.urls import include, url
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from carbondoomsday.measurements import urls

schema_view = get_schema_view(
   openapi.Info(
      title='CarbonDoomsDay Web API',
      default_version='v1',
      description=(
        'A real-time RESTish web API for '
        'worldwide carbon dioxide levels.'
      ),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include(urls)),
    url(
        r"^",
        schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui'
    ),
]
