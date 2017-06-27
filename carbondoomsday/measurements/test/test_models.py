"""Model tests."""

from datetime import date
from decimal import Decimal

import pytest
from django.db.utils import IntegrityError

from carbondoomsday.measurements.models import CO2

pytestmark = pytest.mark.django_db(transaction=True)


def test_co2():
    today, ppm = date.today(), Decimal('449.15')
    co2 = CO2.objects.create(date=today, ppm=ppm)

    created = CO2.objects.get(date=str(co2.date))
    assert created.date == today
    assert created.ppm == ppm

    with pytest.raises(IntegrityError):
        CO2.objects.create(date=today, ppm=None)

    with pytest.raises(IntegrityError):
        CO2.objects.create(date=today, ppm=ppm)
