"""Model testing."""

from datetime import date

import pytest
from django.db.utils import IntegrityError

from carbondoomsday.carbondioxide.models import CO2Measurement

pytestmark = pytest.mark.django_db(transaction=True)


def test_co2_measurement():
    today = date.today()
    ppm = 449.15

    co2 = CO2Measurement.objects.create(date=today, ppm=ppm)
    assert co2.date == today
    assert co2.ppm == ppm

    with pytest.raises(IntegrityError):
        CO2Measurement.objects.create(date=today, ppm=None)

    with pytest.raises(IntegrityError):
        CO2Measurement.objects.create(date=today, ppm=ppm)
