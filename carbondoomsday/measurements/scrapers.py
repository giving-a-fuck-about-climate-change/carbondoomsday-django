"""Data scrapers. If adding one, implement the abstract class."""

import csv
import datetime
from abc import ABC, abstractmethod
from datetime import datetime as dt
from decimal import Decimal, InvalidOperation
from urllib.request import urlopen

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from carbondoomsday.measurements.models import CO2


class AbstractScraper(ABC):
    """An abstract class for specifying scraping behaviour."""
    @abstractmethod
    def get_from_network(self, location):
        """Retrieve the data set over the network."""

    @abstractmethod
    def parse_data_set(self, response):
        """Parse the received data set."""

    @abstractmethod
    def parse_values(self, entries):
        """Retrieve the values from the data set."""

    def handle_values(self, values):
        """Get the parsed values into the database.

        If it's a new value pair, create it. If there is an
        existing measurement, make sure we update our stored
        PPM value. This ensures consistency with our data
        sources.
        """
        for new_date, new_ppm in values:
            try:
                existing_measurement = CO2.objects.get(date=new_date)
                if not existing_measurement.ppm == new_ppm:
                    existing_measurement.ppm = new_ppm
                    existing_measurement.save()
            except ObjectDoesNotExist:
                CO2.objects.create(date=new_date, ppm=new_ppm)

    def run(self, location):
        """Run the scraper."""
        response = self.get_from_network(location)
        entries = self.parse_data_set(response)
        values = self.parse_values(entries)
        self.handle_values(values)


class DailyMLOCO2Since2015(AbstractScraper):
    """Daily CO2 measurements from the Mauna Loa Observatory since 2015."""
    def __str__(self):
        """Human readable representation."""
        return "daily-mlo-co2-since-2015"

    def get_from_network(self, location):
        """Retrieve the data set over the network."""
        return requests.get(location)

    def parse_data_set(self, response):
        """Parse the received data set."""
        decoded = str(response.content, 'utf-8')
        separated = decoded.split('\n')
        parsed = list(csv.reader(separated))
        drop_headers = slice(1, len(parsed))
        return parsed[drop_headers]

    def parse_values(self, entries):
        """Retrieve the values from the data set."""
        values = []
        for entry in entries:
            if not entry:
                continue

            date, daily, _, _ = entry
            try:
                separated = date.split('-', 2)
                intified = map(int, separated)
                co2_date = datetime.date(*intified)
            except (ValueError, TypeError):
                continue

            try:
                co2_ppm = Decimal(daily)
            except InvalidOperation:
                continue

            values.append((co2_date, co2_ppm))

        return values

    def run(self, location):
        """Run the scraper."""
        response = self.get_from_network(location)
        entries = self.parse_data_set(response)
        values = self.parse_values(entries)

        pre_count = CO2.objects.count()
        self.handle_values(values)
        post_count = CO2.objects.count()
        num_inserted = post_count - pre_count

        self.notify(num_inserted)

    def notify(self, inserted):
        """Notify Gitter after task success."""
        if settings.ENVIRONMENT == 'Development' or inserted == 0:
            return
        args = (settings.ENVIRONMENT, str(self), inserted)
        msg = "{}: {} added {} CO2 measurements just now"
        payload = {'message': msg.format(*args)}
        requests.post(settings.GITTER_URL, data=payload)


class DailyMLOCO2Since1974(AbstractScraper):
    """Daily CO2 measurements from the Mauna Loa Observatory since 1974."""
    def get_from_network(self, location):
        """Retrieve the text file."""
        return urlopen(location).read()

    def parse_data_set(self, response):
        """Parse the CO2 measurements text based data set."""
        decoded = str(response, 'utf-8')
        separated = decoded.split('\n')
        return [line for line in separated if line.startswith('MLO')]

    def parse_values(self, entries):
        """Retrieve the values from the data set."""
        values = []

        NOT_RECORDED = '-999.99'
        PPM_HEADER = 7
        time_of_year = slice(1, 4)

        for entry in entries:
            try:
                year, month, day = entry.split()[time_of_year]
                intified = map(int, (year, month, day))
                co2_date = datetime.date(*intified)
            except (ValueError, TypeError):
                continue

            try:
                daily = entry.split()[PPM_HEADER]
                if daily == NOT_RECORDED:
                    continue
                co2_ppm = Decimal(daily)
            except (InvalidOperation, IndexError, ValueError, TypeError):
                continue

            values.append((co2_date, co2_ppm))

        return values


class DailyMLOCO2Since1958(AbstractScraper):
    """Daily CO2 measurements from the Mauna Loa Observatory since 1958."""
    def get_from_network(self, location):
        """Retrieve the CSV file."""
        return requests.get(location)

    def parse_data_set(self, response):
        """Parse the CO2 measurements CSV data set."""
        decoded = str(response.content, 'utf-8')
        separated = decoded.split('\n')
        return list(csv.reader(separated))

    def parse_values(self, entries):
        """Create new CO2 measurements."""
        values = []

        for entry in entries:
            try:
                co2_date = dt.strptime(entry[0], '%Y-%m-%d')
            except (ValueError, IndexError):
                continue

            try:
                co2_ppm = Decimal(entry[1])
            except (InvalidOperation, IndexError):
                continue

            values.append((co2_date, co2_ppm))

        return values
