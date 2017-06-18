"""Database models."""

from django.db import models


class CO2Measurement(models.Model):
    """CO2 measurement model."""
    date = models.DateField(unique=True)
    ppm = models.DecimalField(max_digits=5, decimal_places=2)
