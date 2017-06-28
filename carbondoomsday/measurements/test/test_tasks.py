"""Celery task tests."""

import datetime
from decimal import Decimal

import pytest
from requests.exceptions import Timeout

from carbondoomsday.measurements.models import CO2

pytestmark = pytest.mark.django_db


def test_scrape_latest_co2_success(mocked_latest_co2_csv):
    from carbondoomsday.measurements.tasks import scrape_latest_co2

    scrape_latest_co2()

    assert CO2.objects.count() == 4

    expected_date = datetime.date(2017, 6, 10)
    assert CO2.objects.filter(date=expected_date).exists()

    expected_range = CO2.objects.filter(
        ppm__gte=Decimal("409.49"), ppm__lte=Decimal("409.69")
    )
    assert expected_range.count() == 2


def test_scrape_latest_co2_network_failure(mocker):
    from carbondoomsday.measurements.tasks import scrape_latest_co2

    target = "carbondoomsday.measurements.tasks.requests.get"
    with mocker.patch(target, side_effect=Timeout()):
        scrape_latest_co2()
    assert CO2.objects.count() == 0


def test_scrape_latest_co2_parse_date_failure(mocker):
    from carbondoomsday.measurements.tasks import scrape_latest_co2

    mocked = mocker.Mock()
    mocked_latest_co2_csv = "Date,day,month,week\n9999-999-999,,,\n"
    mocked.content = bytes(mocked_latest_co2_csv, "utf-8")
    target = "carbondoomsday.measurements.tasks.requests.get"

    with mocker.patch(target, return_value=mocked):
        scrape_latest_co2()
    assert CO2.objects.count() == 0


def test_scrape_latest_co2_parse_ppm_failure(mocker):
    from carbondoomsday.measurements.tasks import scrape_latest_co2

    mocked = mocker.Mock()
    mocked_latest_co2_csv = "Date,day,month,week\n2017-06-06,x,y,z\n"
    mocked.content = bytes(mocked_latest_co2_csv, "utf-8")
    target = "carbondoomsday.measurements.tasks.requests.get"

    with mocker.patch(target, return_value=mocked):
        scrape_latest_co2()

    assert CO2.objects.count() == 0


def test_scrape_latest_co2_existing_models(mocked_latest_co2_csv):
    from carbondoomsday.measurements.tasks import scrape_latest_co2

    scrape_latest_co2()
    assert CO2.objects.count() == 4
    scrape_latest_co2()
    assert CO2.objects.count() == 4


def test_scrape_historic_co2_success(mocked_historic_co2_csv):
    from carbondoomsday.measurements.tasks import scrape_historic_co2

    scrape_historic_co2()
    assert CO2.objects.count() == 2


def test_scrape_historic_co2_network_failure(mocker):
    from carbondoomsday.measurements.tasks import scrape_historic_co2

    target = "carbondoomsday.measurements.tasks.urlopen"
    with mocker.patch(target, side_effect=Timeout()):
        scrape_historic_co2()
    assert CO2.objects.count() == 0


def test_scrape_historic_co2_parse_date_failure(mocker):
    from carbondoomsday.measurements.tasks import scrape_historic_co2

    mocked = mocker.Mock()
    mocked_historic_co2_csv = bytes("MLO FOO BAR BAZ", "utf-8")
    mocked_function_kwargs = {"read.return_value": mocked_historic_co2_csv}
    mocked.configure_mock(**mocked_function_kwargs)
    target = "carbondoomsday.measurements.tasks.urlopen"

    with mocker.patch(target, return_value=mocked):
        scrape_historic_co2()


def test_scrape_historic_co2_parse_ppm_failure(mocker):
    from carbondoomsday.measurements.tasks import scrape_historic_co2

    mocked = mocker.Mock()
    mocked_historic_co2_csv = bytes("MLO 1974 1 1", "utf-8")
    mocked_function_kwargs = {"read.return_value": mocked_historic_co2_csv}
    mocked.configure_mock(**mocked_function_kwargs)
    target = "carbondoomsday.measurements.tasks.urlopen"

    with mocker.patch(target, return_value=mocked):
        scrape_historic_co2()

    assert CO2.objects.count() == 0


def test_scrape_historic_co2_existing_models(mocked_historic_co2_csv):
    from carbondoomsday.measurements.tasks import scrape_historic_co2

    scrape_historic_co2()
    assert CO2.objects.count() == 2
    scrape_historic_co2()
    assert CO2.objects.count() == 2
