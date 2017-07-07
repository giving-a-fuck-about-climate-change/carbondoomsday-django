"""Command to scrape daily MLO CO2 measurements since 1974."""

from django.core.management.base import BaseCommand

from carbondoomsday.measurements import tasks


class Command(BaseCommand):
    help = 'Scrape daily MLO CO2 measurements since 1974.'

    def handle(self, *args, **options):
        tasks.scrape_mlo_co2_measurements_since_1974()
