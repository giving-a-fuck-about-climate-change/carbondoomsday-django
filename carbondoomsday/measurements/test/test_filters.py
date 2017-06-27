"""View filtering tests."""

from datetime import date
from decimal import Decimal

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db()


def test_co2_filtering(client, co2):
    url = reverse('co2-list')

    response = client.get(url, {'ppm__gte': Decimal('500.00')})
    assert response.json()['count'] == 0

    response = client.get(url, {'ppm__lte': Decimal('500.00')})
    assert response.json()['count'] == 1

    response = client.get(url, {'date__gte': date(2666, 6, 6)})
    assert response.json()['count'] == 0

    response = client.get(url, {'date': co2.date})
    assert response.json()['count'] == 1
