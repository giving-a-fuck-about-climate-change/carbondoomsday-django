"""Model tests."""

from datetime import date
from decimal import Decimal

import pytest
from django.db.utils import IntegrityError

from carbondoomsday.carbondioxide.models import CO2Measurement

pytestmark = pytest.mark.django_db(transaction=True)


def test_co2_measurement():
    today, ppm = date.today(), Decimal("449.15")
    co2 = CO2Measurement.objects.create(date=today, ppm=ppm)

    created = CO2Measurement.objects.get(date=str(co2.date))
    assert created.date == today
    assert created.ppm == ppm

    with pytest.raises(IntegrityError):
        CO2Measurement.objects.create(date=today, ppm=None)

    with pytest.raises(IntegrityError):
        CO2Measurement.objects.create(date=today, ppm=ppm)
