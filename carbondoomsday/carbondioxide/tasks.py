"""Celery tasks module."""

import csv
import datetime
import logging
from decimal import Decimal, InvalidOperation
from urllib.request import urlopen

import requests
from django.conf import settings
from django.db import transaction

from carbondoomsday.celeryconf import app

logger = logging.getLogger(__name__)


@app.task
@transaction.atomic
def scrape_latest():
    """Scrape latest Mauna Loa daily CO2 measurements."""
    from carbondoomsday.carbondioxide.models import CO2Measurement

    try:
        response = requests.get(settings.LATEST_CO2_URL)
    except Exception as err:
        msg = "Failed to retrieve CSV for latest CO2 scrape."
        logger.error(msg)
        return

    logger.info("Retrieved CSV file with latest data.")

    decoded = str(response.content, "utf-8")
    separated = decoded.split("\n")
    parsed = list(csv.reader(separated))

    drop_headers = slice(1, len(parsed))
    without_header = parsed[drop_headers]

    stored, skipped = 0, 0
    for entry in without_header:
        if not entry:
            skipped += 1
            continue

        date, daily, _, _ = entry

        try:
            separated = date.split("-", 2)
            intified = map(int, separated)
            co2_date = datetime.date(*intified)
        except (ValueError, TypeError):
            msg = "Failed to parse date, found '{}'."
            logger.debug(msg.format(date))
            skipped += 1
            continue

        measurement = CO2Measurement.objects.filter(date=co2_date)
        if measurement.exists():
            msg = "Entry for {} already stored. Skipping."
            logger.debug(msg.format(str(co2_date)))
            skipped += 1
            continue

        try:
            co2_ppm = Decimal(daily)
        except InvalidOperation:
            msg = "Failed to convert '{}' to type decimal. Skipping."
            logger.debug(msg.format(daily))
            skipped += 1
            continue

        CO2Measurement.objects.create(date=co2_date, ppm=co2_ppm)
        msg = "Stored new CO2 entry for {} with PPM of {}."
        logger.info(msg.format(str(co2_date), str(co2_ppm)))
        stored += 1

    logger.info("Initially parsed {} entries.".format(len(without_header)))
    logger.info("Stored {}. Skipped {}.".format(stored, skipped))


@app.task
@transaction.atomic
def scrape_historic():
    """Scrape historical Mauna Loa CO2 measurements."""
    from carbondoomsday.carbondioxide.models import CO2Measurement

    try:
        handler = urlopen(settings.HISTORIC_CO2_URL)
        response = handler.read()
    except Exception as err:
        logger.error("Failed to retrieve CSV for historic CO2 scrape.")
        logger.error("Saw the following error: {}".format(str(err)))
        return

    logger.info("Retrieved CSV file with latest data.")

    decoded = str(response, "utf-8")
    separated = decoded.split("\n")
    uncommented = [line for line in separated if line.startswith("MLO")]

    stored, skipped = 0, 0
    for line in uncommented:
        try:
            time_of_year = slice(1, 4)
            year, month, day = line.split()[time_of_year]
            intified = map(int, (year, month, day))
            co2_date = datetime.date(*intified)
        except (ValueError, TypeError):
            msg = "Failed to parse entry, found '{}'."
            logger.debug(msg.format(line))
            skipped += 1
            continue

        measurement = CO2Measurement.objects.filter(date=co2_date)
        if measurement.exists():
            msg = "Entry for {} already stored. Skipping."
            logger.debug(msg.format(str(co2_date)))
            skipped += 1
            continue

        NOT_RECORDED = "-999.99"
        PPM_HEADER = 7
        try:
            daily = line.split()[PPM_HEADER]
            if daily == NOT_RECORDED:
                msg = "{} marked as not recorded. Skipping."
                logger.debug(msg.format(co2_date))
                skipped += 1
                continue
            co2_ppm = Decimal(daily)
        except (InvalidOperation, IndexError, ValueError, TypeError):
            msg = "Failed to convert '{}' to type decimal. Skipping."
            logger.debug(msg.format(line))
            skipped += 1
            continue

        CO2Measurement.objects.create(date=co2_date, ppm=co2_ppm)
        stored += 1

        msg = "Stored new CO2 entry for {} with PPM of {}"
        logger.info(msg.format(str(co2_date), str(co2_ppm)))

    logger.info("Initially parsed {} entries.".format(len(uncommented)))
    logger.info("Stored {}. Skipped {}.".format(stored, skipped))
