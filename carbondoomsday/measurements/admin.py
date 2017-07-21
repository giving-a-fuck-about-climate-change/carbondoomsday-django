"""Admin models."""

from django.contrib import admin

from carbondoomsday.measurements.models import CO2


@admin.register(CO2)
class CO2Admin(admin.ModelAdmin):
    readonly_fields = ('date', 'ppm', 'created',)
    list_display = ('date', 'ppm', 'created',)
    list_filter = ('created',)
    ordering = ('-date',)
