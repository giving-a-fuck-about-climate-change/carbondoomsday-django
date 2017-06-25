"""Web API middleware tests."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_middleware_cors_header(client, co2_measurement):
    url = reverse("co2measurement-list")
    response = client.get(url, HTTP_ORIGIN="http://www.foobar.com")
    assert response["Access-Control-Allow-Origin"] == "*"
