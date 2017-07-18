"""Asynchronous Celery tasks."""


from django.conf import settings
from django.db import transaction

from carbondoomsday.celeryconf import app
from carbondoomsday.measurements.scrapers import (
    DailyMLOCO2Since1958, DailyMLOCO2Since1974, DailyMLOCO2Since2015
)


@app.task
@transaction.atomic
def scrape_mlo_co2_measurements_since_2015():
    """Scrape daily CO2 measurements from MLO since 2015."""
    scraper = DailyMLOCO2Since2015()
    scraper.run(settings.MLO_DAILY_CO2_2015_TO_2017)


@app.task
@transaction.atomic
def scrape_mlo_co2_measurements_since_1974():
    """Scrape daily CO2 measurements from MLO since 1974."""
    scraper = DailyMLOCO2Since1974()
    scraper.run(settings.MLO_DAILY_CO2_1974_TO_2017)


@app.task
@transaction.atomic
def scrape_mlo_co2_measurements_since_1958():
    """Scrape daily CO2 measurements from MLO since 1958."""
    scraper = DailyMLOCO2Since1958()
    scraper.run(settings.MLO_DAILY_CO2_1958_TO_2017)
