"""Web API view tests."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_co2_ready_only_view(client, co2_measurement):
    url = reverse("co2measurement-list")

    assert client.post(url).status_code == 405
    assert client.put(url).status_code == 405
    assert client.patch(url).status_code == 405

    response = client.get(url)
    assert response.json()['count'] == 1

    first = response.json()['results'][0]
    assert first['ppm'] == str(co2_measurement.ppm)
    assert first['date'] == str(co2_measurement.date)

    url = reverse("co2measurement-detail", args=(str(co2_measurement.date),))
    response = client.get(url)
    assert response.json()['ppm'] == str(co2_measurement.ppm)
