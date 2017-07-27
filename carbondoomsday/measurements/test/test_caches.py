"""Web API view cache tests."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_co2_cache_control_enabled(client, co2):
    url = reverse('co2-detail', args=(str(co2.date),))
    response = client.get(url)
    assert response['cache-control']
