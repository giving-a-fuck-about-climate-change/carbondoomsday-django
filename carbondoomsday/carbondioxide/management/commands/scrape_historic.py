"""Command to scrape the Mauna Loa historical CO2 measurements."""

from django.core.management.base import BaseCommand

from carbondoomsday.carbondioxide import tasks


class Command(BaseCommand):
    help = "Scrape the Mauna Loa historical CO2 measurements."

    def handle(self, *args, **options):
        tasks.scrape_historic()
