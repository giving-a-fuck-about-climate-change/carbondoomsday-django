"""Celery task tests."""

import datetime
import os
from decimal import Decimal

import pytest
from django.conf import settings

from carbondoomsday.email_signature import utils
from carbondoomsday.measurements.models import CO2

pytestmark = pytest.mark.django_db


def test_update_email_signature(mocker):
    from carbondoomsday.email_signature.utils import (
        update_email_signature
    )

    ppm = Decimal('100.00')
    CO2.objects.create(date=datetime.date.today(), ppm=ppm)
    spy = mocker.spy(utils, 'create_email_signature')
    update_email_signature()
    spy.assert_called_once_with(ppm)


def test_create_email_signature(mocker):
    from carbondoomsday.email_signature.utils import (
        create_email_signature
    )

    ppm = Decimal('100.00')
    CO2.objects.create(date=datetime.date.today(), ppm=ppm)
    create_email_signature(ppm)
    created = os.path.getmtime(
            settings.MEDIA_ROOT + '/carbondoomsday_email_signature.png')
    create_email_signature(ppm)
    updated = os.path.getmtime(
            settings.MEDIA_ROOT + '/carbondoomsday_email_signature.png')
    assert updated > created


def test_update_email_signature_task(mocker):
    from carbondoomsday.email_signature.tasks import (
        update_email_signature_task
    )
    target = 'carbondoomsday.email_signature.tasks.update_email_signature'
    patch = mocker.patch(target)
    update_email_signature_task()
    patch.assert_called_once_with()
