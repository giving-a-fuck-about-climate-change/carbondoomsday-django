"""URL configuration."""

from django.conf.urls import url  # , include
from django.contrib import admin

# from carbondoomsday import carbondioxide

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    # url(r"^api/", include(carbondioxide.urls))
]
