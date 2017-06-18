"""Celery tasks module."""

import csv
import datetime
import logging
from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings
from django.db import transaction

from carbondoomsday.celery import app


@app.task
@transaction.atomic
def scrape_latest():
    """Scrape the latest CO2 measurements."""
    from carbondoomsday.carbondioxide.models import CO2Measurement

    try:
        response = requests.get(settings.LATEST_CO2_URL)
    except Exception as err:
        logging.error("Failed to retrieve CSV for latest CO2 scrape.")
        raise err

    decoded = str(response.content, "utf-8")
    separated = decoded.split("\n")
    parsed = list(csv.reader(separated))

    drop_headers = slice(1, len(parsed))
    for entry in parsed[drop_headers]:
        if not entry:
            continue

        date, daily, _, _ = entry

        try:
            separated = date.split("-", 2)
            intified = map(int, separated)
            co2_date = datetime.date(*intified)
        except (ValueError, TypeError):
            msg = "Failed to parse date, found '{}'".format(date)
            logging.error(msg)
            continue

        try:
            co2_ppm = Decimal(daily)
        except InvalidOperation:
            continue

        measurement = CO2Measurement.objects.filter(date=co2_date)
        if measurement.exists():
            continue

        CO2Measurement.objects.create(date=co2_date, ppm=co2_ppm)
