"""Database models."""

from django.db import models


class CO2Measurement(models.Model):
    date = models.DateField(unique=True)
    ppm = models.DecimalField(max_digits=5, decimal_places=2)
