"""View ordering tests."""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db()


def test_always_date_reverse_descending_order(client, today):
    from carbondoomsday.measurements.models import CO2

    yesterday = today - timedelta(days=1)
    CO2.objects.create(date=yesterday, ppm=Decimal('448.00'))

    CO2.objects.create(date=today, ppm=Decimal('449.00'))

    url = reverse('co2-list')
    response = client.get(url)

    assert response.json()['results'][0]['date'] == str(today)
    assert response.json()['results'][1]['date'] == str(yesterday)
