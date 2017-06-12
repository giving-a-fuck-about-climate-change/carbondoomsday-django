"""Celery tasks module."""

from carbondoomsday.celery import app


@app.task
def scrape_last_five_days():
    print("Scrape that data!")
