"""View filtering tests."""

from datetime import date
from decimal import Decimal

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db()


def test_co2_filtering(client, co2_measurement):
    url = reverse("co2measurement-list")

    response = client.get(url, {"ppm__gte": Decimal("500.00")})
    assert len(response.json()) == 0

    response = client.get(url, {"ppm__lte": Decimal("500.00")})
    assert len(response.json()) == 1

    response = client.get(url, {"date__gte": date(2666, 6, 6)})
    assert len(response.json()) == 0

    response = client.get(url, {"date": co2_measurement.date})
    assert len(response.json()) == 1
