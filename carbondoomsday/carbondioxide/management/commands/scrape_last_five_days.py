"""Command to scrape the last 5 days worth of CO2 measurements."""

from django.core.management.base import BaseCommand

from carbondoomsday.carbondioxide import tasks


class Command(BaseCommand):
    help = "Scrape the last 5 days worth of CO2 measurements"

    def handle(self, *args, **options):
        tasks.scrape_last_five_days()
