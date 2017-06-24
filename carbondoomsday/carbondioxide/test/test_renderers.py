"""Renderer tests."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_csv_renderer(client, co2_measurement):
    url = reverse("co2measurement-list")

    response = client.get(url, HTTP_ACCEPT="application/json")
    assert response.accepted_media_type == "application/json"

    response = client.get(url, HTTP_ACCEPT="text/csv")
    assert response.accepted_media_type == "text/csv"
