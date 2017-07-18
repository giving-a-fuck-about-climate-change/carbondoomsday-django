"""Data scrapers. If adding one, implement the abstract class."""

import csv
import datetime
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from urllib.request import urlopen

import requests

from carbondoomsday.measurements.models import CO2


class AbstractScraper(ABC):
    """An abstract class for specifying scraping behaviour."""
    @abstractmethod
    def retrieve(self, location):
        """Retrieve the data set over the network."""

    @abstractmethod
    def parse(self, response):
        """Parse the received data set."""

    @abstractmethod
    def insert(self, entry):
        """Insert the parsed data into the database."""

    def run(self, location):
        """Run the scraper."""
        response = self.retrieve(location)
        parsed = self.parse(response)
        self.insert(parsed)


class DailyMLOCO2Since2015(AbstractScraper):
    """Daily CO2 measurements from the Mauna Loa Observatory since 2015."""
    def retrieve(self, location):
        """Retrieve the data set over the network."""
        return requests.get(location)

    def parse(self, response):
        """Parse the CO2 measurements CSV based data set."""
        decoded = str(response.content, 'utf-8')
        separated = decoded.split('\n')
        parsed = list(csv.reader(separated))
        drop_headers = slice(1, len(parsed))
        return parsed[drop_headers]

    def insert(self, parsed):
        """Create new CO2 measurements."""
        for entry in parsed:
            if not entry:
                return

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

            if not CO2.objects.filter(date=co2_date).exists():
                CO2.objects.create(date=co2_date, ppm=co2_ppm)


class DailyMLOCO2Since1974(AbstractScraper):
    """Daily CO2 measurements from the Mauna Loa Observatory since 1974."""
    def retrieve(self, location):
        """Retrieve the text file."""
        return urlopen(location).read()

    def parse(self, response):
        """Parse the CO2 measurements text based data set."""
        decoded = str(response, 'utf-8')
        separated = decoded.split('\n')
        return [line for line in separated if line.startswith('MLO')]

    def insert(self, parsed):
        """Create new CO2 measurements."""
        NOT_RECORDED = '-999.99'
        PPM_HEADER = 7
        time_of_year = slice(1, 4)
        for entry in parsed:
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

            if not CO2.objects.filter(date=co2_date).exists():
                CO2.objects.create(date=co2_date, ppm=co2_ppm)


class DailyMLOCO2Since1958(AbstractScraper):
    """Daily CO2 measurements from the Mauna Loa Observatory since 1958."""
    def retrieve(self, location):
        """Retrieve the CSV file."""
        return requests.get(location)

    def parse(self, response):
        """Parse the CO2 measurements CSV data set."""
        decoded = str(response.content, 'utf-8')
        separated = decoded.split('\n')
        return list(csv.reader(separated))

    def insert(self, parsed):
        """Create new CO2 measurements."""
        for entry in parsed:
            try:
                co2_date = dt.strptime(entry[0], '%Y-%m-%d')
            except (ValueError, IndexError):
                continue

            try:
                co2_ppm = Decimal(entry[1])
            except (InvalidOperation, IndexError):
                continue

            if not CO2.objects.filter(date=co2_date).exists():
                CO2.objects.create(date=co2_date, ppm=co2_ppm)
