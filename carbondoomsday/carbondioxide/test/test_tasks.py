"""Celery task tests."""

import datetime
from decimal import Decimal

import pytest
from requests.exceptions import Timeout

from carbondoomsday.carbondioxide.models import CO2Measurement

pytestmark = pytest.mark.django_db


def test_scrape_latest_success(mocked_latest_co2_csv):
    from carbondoomsday.carbondioxide.tasks import scrape_latest

    scrape_latest()

    assert CO2Measurement.objects.count() == 4

    expected_date = datetime.date(2017, 6, 10)
    assert CO2Measurement.objects.filter(date=expected_date).exists()

    expected_range = CO2Measurement.objects.filter(
        ppm__gte=Decimal("409.49"), ppm__lte=Decimal("409.69")
    )
    assert expected_range.count() == 2


def test_scrape_latest_network_failure(mocker, caplog):
    from carbondoomsday.carbondioxide.tasks import scrape_latest

    target = "carbondoomsday.carbondioxide.tasks.requests.get"
    mocker.patch(target, side_effect=Timeout())

    assert scrape_latest() is None

    expected_msg = "Failed to retrieve CSV"
    assert any((expected_msg in rec.msg for rec in caplog.records()))


def test_scrape_latest_parse_date_failure(mocker, caplog):
    from carbondoomsday.carbondioxide.tasks import scrape_latest

    mocked = mocker.Mock()
    target = "carbondoomsday.carbondioxide.tasks.requests.get"

    mocked_latest_co2_csv = "Date,day,month,week\n9999-999-999,,,\n"
    mocked.content = bytes(mocked_latest_co2_csv, "utf-8")

    with mocker.patch(target, return_value=mocked):
        scrape_latest()

    expected_msg = "Failed to parse date"
    assert any((expected_msg in rec.msg for rec in caplog.records()))


def test_scrape_latest_parse_ppm_failure(mocker):
    from carbondoomsday.carbondioxide.tasks import scrape_latest

    mocked = mocker.Mock()
    target = "carbondoomsday.carbondioxide.tasks.requests.get"

    mocked_latest_co2_csv = "Date,day,month,week\n2017-06-06,x,y,z\n"
    mocked.content = bytes(mocked_latest_co2_csv, "utf-8")

    with mocker.patch(target, return_value=mocked):
        scrape_latest()

    assert CO2Measurement.objects.count() == 0


def test_scrape_latest_existing_models(mocked_latest_co2_csv):
    from carbondoomsday.carbondioxide.tasks import scrape_latest

    scrape_latest()
    assert CO2Measurement.objects.count() == 4
    scrape_latest()
    assert CO2Measurement.objects.count() == 4


def test_scrape_historic_success(mocked_historic_co2_csv):
    from carbondoomsday.carbondioxide.tasks import scrape_historic

    scrape_historic()
    assert CO2Measurement.objects.count() == 2


def test_scrape_historic_network_failure(mocker, caplog):
    from carbondoomsday.carbondioxide.tasks import scrape_historic

    target = "carbondoomsday.carbondioxide.tasks.requests.get"
    mocker.patch(target, side_effect=Timeout())

    assert scrape_historic() is None

    expected_msg = "Failed to retrieve CSV"
    assert any((expected_msg in rec.msg for rec in caplog.records()))


def test_scrape_historic_parse_date_failure(mocker, caplog):
    from carbondoomsday.carbondioxide.tasks import scrape_historic

    mocked = mocker.Mock()
    target = "carbondoomsday.carbondioxide.tasks.requests.get"

    mocked_historic_co2_csv = "MLO FOO BAR BAZ"
    mocked.content = bytes(mocked_historic_co2_csv, "utf-8")

    with mocker.patch(target, return_value=mocked):
        scrape_historic()

    expected_msg = "Failed to parse entry"
    assert any((expected_msg in rec.msg for rec in caplog.records()))


def test_scrape_historic_parse_ppm_failure(mocker):
    from carbondoomsday.carbondioxide.tasks import scrape_historic

    mocked = mocker.Mock()
    target = "carbondoomsday.carbondioxide.tasks.requests.get"

    mocked_historic_co2_csv = "MLO 1974 1 1"
    mocked.content = bytes(mocked_historic_co2_csv, "utf-8")

    with mocker.patch(target, return_value=mocked):
        scrape_historic()

    assert CO2Measurement.objects.count() == 0


def test_scrape_historic_existing_models(mocked_historic_co2_csv):
    from carbondoomsday.carbondioxide.tasks import scrape_historic

    scrape_historic()
    assert CO2Measurement.objects.count() == 2
    scrape_historic()
    assert CO2Measurement.objects.count() == 2
