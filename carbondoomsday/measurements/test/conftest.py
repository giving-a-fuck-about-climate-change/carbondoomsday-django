"""Test fixtures."""

from datetime import date
from decimal import Decimal

import pytest
from freezegun import freeze_time
from rest_framework.test import APIClient

from carbondoomsday.measurements.models import CO2


@pytest.fixture
def mlo_co2_since_2015(mocker):
    mocked_csv = (
        'Date,day,month,week\n'
        '2017-06-08,409.49,409.65,409.65\n'
        '2017-06-09,409.69,,409.65\n'
        '2017-06-10,409.15,,409.65\n'
        '2017-06-11,,,\n'
        '2017-06-12,409.75,,\n'
    )

    mocked = mocker.Mock()
    mocked.content = bytes(mocked_csv, 'utf-8')
    target = 'carbondoomsday.measurements.scrapers.requests.get'
    mocker.patch(target, return_value=mocked)


@pytest.fixture
def mlo_co2_since_1974(mocker):
    mocked_csv = (
        '# FOO\n'
        'MLO 1974 1 1 0 0 0 -999.99 -99.99 0 19.536 '
        '-155.576 3437.0 3397.0 40.0 NA ...\n'
        'MLO 1974 9 17 0 0 0 326.832 0.235 6 19.536 '
        '-155.576 3437.0 3397.0 40.0 NA ...\n'
        'MLO 1974 12 25 0 0 0 329.775 0.136 21 19.536 '
        '-155.576 3437.0 3397.0 40.0 NA *..\n'
    )

    mocked = mocker.Mock()
    mocked_function_kwargs = {'read.return_value': bytes(mocked_csv, 'utf-8')}
    mocked.configure_mock(**mocked_function_kwargs)
    target = 'carbondoomsday.measurements.scrapers.urlopen'
    mocker.patch(target, return_value=mocked)


@pytest.fixture
def co2():
    today, ppm = date.today(), Decimal('449.15')
    return CO2.objects.create(date=today, ppm=ppm)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def today():
    today = date.today()
    with freeze_time(today):
        yield today
