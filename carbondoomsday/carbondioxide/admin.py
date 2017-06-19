"""Admin models."""

from carbondoomsday.carbondioxide.models import CO2Measurement
from django.contrib import admin


@admin.register(CO2Measurement)
class CO2MeasurementAdmin(admin.ModelAdmin):
    readonly_fields = ("date", "ppm",)
