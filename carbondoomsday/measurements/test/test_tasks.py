"""Celery task tests."""

import datetime
from decimal import Decimal

import pytest
from requests.exceptions import Timeout

from carbondoomsday.measurements.models import CO2

pytestmark = pytest.mark.django_db


def test_scrape_daily_mlo_co2_since_2015(mlo_co2_since_2015):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_2015
    )

    scrape_mlo_co2_measurements_since_2015()

    assert CO2.objects.count() == 4

    expected_date = datetime.date(2017, 6, 10)
    assert CO2.objects.filter(date=expected_date).exists()

    expected_range = CO2.objects.filter(
        ppm__gte=Decimal("409.49"), ppm__lte=Decimal("409.69")
    )
    assert expected_range.count() == 2


def test_scrape_daily_mlo_co2_since_2015_network_failure(mocker):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_2015
    )

    target = "carbondoomsday.measurements.scrapers.requests.get"
    with mocker.patch(target, side_effect=Timeout()):
        with pytest.raises(Timeout):
            scrape_mlo_co2_measurements_since_2015()
    assert CO2.objects.count() == 0


def test_scrape_daily_mlo_co2_since_2015_parse_skip(mocker):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_2015
    )

    mocked = mocker.Mock()
    mocked_co2_csv = "Date,day,month,week\n9999-999-999,,,\n"
    mocked.content = bytes(mocked_co2_csv, "utf-8")
    target = "carbondoomsday.measurements.scrapers.requests.get"
    with mocker.patch(target, return_value=mocked):
        scrape_mlo_co2_measurements_since_2015()
    assert CO2.objects.count() == 0

    mocked = mocker.Mock()
    mocked_co2_csv = "Date,day,month,week\n2017-06-06,x,y,z\n"
    mocked.content = bytes(mocked_co2_csv, "utf-8")
    target = "carbondoomsday.measurements.scrapers.requests.get"
    with mocker.patch(target, return_value=mocked):
        scrape_mlo_co2_measurements_since_2015()
    assert CO2.objects.count() == 0


def test_scrape_daily_mlo_co2_since_2015_existing_models(mlo_co2_since_2015):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_2015
    )

    scrape_mlo_co2_measurements_since_2015()
    assert CO2.objects.count() == 4
    scrape_mlo_co2_measurements_since_2015()
    assert CO2.objects.count() == 4


def test_scrape_daily_mlo_co2_since_1974(mlo_co2_since_1974):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1974
    )

    scrape_mlo_co2_measurements_since_1974()
    assert CO2.objects.count() == 2


def test_scrape_daily_mlo_co2_since_1974_network_failure(mocker):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1974
    )

    target = "carbondoomsday.measurements.scrapers.urlopen"
    with mocker.patch(target, side_effect=Timeout()):
        with pytest.raises(Timeout):
            scrape_mlo_co2_measurements_since_1974()
    assert CO2.objects.count() == 0


def test_scrape_daily_mlo_co2_since_1974_parse_skip(mocker):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1974
    )

    mocked = mocker.Mock()
    mocked_co2_csv = bytes("MLO FOO BAR BAZ", "utf-8")
    mocked_function_kwargs = {"read.return_value": mocked_co2_csv}
    mocked.configure_mock(**mocked_function_kwargs)
    target = "carbondoomsday.measurements.scrapers.urlopen"
    with mocker.patch(target, return_value=mocked):
        scrape_mlo_co2_measurements_since_1974()
    assert CO2.objects.count() == 0

    mocked = mocker.Mock()
    mocked_co2_csv = bytes("MLO 1974 1 1", "utf-8")
    mocked_function_kwargs = {"read.return_value": mocked_co2_csv}
    mocked.configure_mock(**mocked_function_kwargs)
    target = "carbondoomsday.measurements.scrapers.urlopen"
    with mocker.patch(target, return_value=mocked):
        scrape_mlo_co2_measurements_since_1974()
    assert CO2.objects.count() == 0


def test_scrape_daily_mlo_co2_since_1974_existing_models(mlo_co2_since_1974):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1974
    )

    scrape_mlo_co2_measurements_since_1974()
    assert CO2.objects.count() == 2
    scrape_mlo_co2_measurements_since_1974()
    assert CO2.objects.count() == 2


def test_scrape_daily_mlo_co2_since_1958(mlo_co2_since_1958):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1958
    )

    scrape_mlo_co2_measurements_since_1958()

    assert CO2.objects.count() == 2

    expected_date = datetime.date(2017, 6, 24)
    expected_ppm = Decimal("408.42")
    assert CO2.objects.filter(
        date=expected_date, ppm=expected_ppm
    ).exists()


def test_scrape_daily_mlo_co2_since_1958_network_failure(mocker):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1958
    )

    target = "carbondoomsday.measurements.scrapers.requests.get"
    with mocker.patch(target, side_effect=Timeout()):
        with pytest.raises(Timeout):
            scrape_mlo_co2_measurements_since_1958()
    assert CO2.objects.count() == 0


def test_scrape_daily_mlo_co2_since_1958_parse_skip(mocker):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1958
    )

    mocked = mocker.Mock()
    mocked_co2_csv = "foobar\n9999-999-999, 408.92"
    mocked.content = bytes(mocked_co2_csv, "utf-8")
    target = "carbondoomsday.measurements.scrapers.requests.get"
    with mocker.patch(target, return_value=mocked):
        scrape_mlo_co2_measurements_since_1958()
    assert CO2.objects.count() == 0

    mocked = mocker.Mock()
    mocked_co2_csv = "foobar\n2017-01-02, barbaz"
    mocked.content = bytes(mocked_co2_csv, "utf-8")
    target = "carbondoomsday.measurements.scrapers.requests.get"
    with mocker.patch(target, return_value=mocked):
        scrape_mlo_co2_measurements_since_1958()
    assert CO2.objects.count() == 0


def test_scrape_daily_mlo_co2_since_1958_existing_models(mlo_co2_since_1958):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1958
    )

    scrape_mlo_co2_measurements_since_1958()
    assert CO2.objects.count() == 2
    scrape_mlo_co2_measurements_since_1958()
    assert CO2.objects.count() == 2


def test_scrape_will_update_existing_values_from_mlo(mlo_co2_since_1958):
    from carbondoomsday.measurements.tasks import (
        scrape_mlo_co2_measurements_since_1958
    )

    assert CO2.objects.count() == 0

    scrape_mlo_co2_measurements_since_1958()
    assert CO2.objects.count() == 2

    co2_measurement = CO2.objects.get(ppm=Decimal('407.77'))
    co2_measurement.ppm = Decimal('666.66')
    co2_measurement.save()

    assert not CO2.objects.filter(ppm=Decimal('407.77')).exists()

    scrape_mlo_co2_measurements_since_1958()
    assert CO2.objects.count() == 2

    assert CO2.objects.filter(ppm=Decimal('407.77')).exists()
    assert not CO2.objects.filter(ppm=Decimal('666.66')).exists()
