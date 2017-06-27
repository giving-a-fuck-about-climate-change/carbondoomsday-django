"""Web API routes."""

from rest_framework.routers import DefaultRouter

from carbondoomsday.measurements import views

router = DefaultRouter()

router.register(r'co2', views.CO2ViewSet)

urlpatterns = router.urls
