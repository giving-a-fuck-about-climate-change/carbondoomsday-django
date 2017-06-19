"""Database models."""

from django.db import models


class CO2Measurement(models.Model):
    """CO2 measurement model."""
    class Meta:
        verbose_name = "CO2 Measurement "
        verbose_name_plural = "CO2 Measurements"

    date = models.DateField(unique=True)
    ppm = models.DecimalField(max_digits=5, decimal_places=2)
