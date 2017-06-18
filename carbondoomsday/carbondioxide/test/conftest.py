"""Test fixtures."""

import pytest


@pytest.fixture
def mocked_co2_csv(mocker):
    mocked_csv = (
        "Date,day,month,week\n"
        "2017-06-08,409.49,409.65,409.65\n"
        "2017-06-09,409.69,,409.65\n"
        "2017-06-10,409.15,,409.65\n"
        "2017-06-11,,,\n"
        "2017-06-12,409.75,,\n"
    )

    mocked = mocker.Mock()
    mocked.content = bytes(mocked_csv, "utf-8")
    target = "carbondoomsday.carbondioxide.tasks.requests.get"
    mocker.patch(target, return_value=mocked)
