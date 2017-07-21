"""Database models."""

from django.db import models


class CO2(models.Model):
    """CO2 measurement model."""
    class Meta:
        verbose_name = "CO2"
        verbose_name_plural = "CO2s"

    date = models.DateField(unique=True)
    ppm = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        """Human readable representation."""
        date, ppm = str(self.date), str(self.ppm)
        return '<CO2 date={}, ppm={}>'.format(date, ppm)
