"""Web API view tests."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_co2_ready_only_view(client, co2):
    url = reverse('co2-list')

    assert client.post(url).status_code == 405
    assert client.put(url).status_code == 405
    assert client.patch(url).status_code == 405

    response = client.get(url)
    assert response.json()['count'] == 1

    first = response.json()['results'][0]
    assert first['ppm'] == str(co2.ppm)
    assert first['date'] == str(co2.date)

    url = reverse('co2-detail', args=(str(co2.date),))
    response = client.get(url)
    assert response.json()['ppm'] == str(co2.ppm)
