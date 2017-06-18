"""Web API routes."""

from rest_framework.routers import DefaultRouter

from carbondoomsday.carbondioxide import views

router = DefaultRouter()

router.register(r"co2", views.CO2MeasurementViewSet)

urlpatterns = router.urls
