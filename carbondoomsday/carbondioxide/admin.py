"""Admin models."""

from django.contrib import admin

from carbondoomsday.carbondioxide.models import CO2Measurement


@admin.register(CO2Measurement)
class CO2MeasurementAdmin(admin.ModelAdmin):
    readonly_fields = ("date", "ppm",)
