"""Command to scrape the latest CO2 measurements."""

from django.core.management.base import BaseCommand

from carbondoomsday.measurements import tasks


class Command(BaseCommand):
    help = 'Scrape the latest CO2 measurements.'

    def handle(self, *args, **options):
        tasks.scrape_latest()
