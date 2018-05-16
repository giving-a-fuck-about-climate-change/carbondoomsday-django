"""Asynchronous Celery tasks."""


from django.db import transaction

from carbondoomsday.celeryconf import app
from carbondoomsday.email_signature.utils import update_email_signature


@app.task
@transaction.atomic
def update_email_signature_task():
    """Update email signature png with the latest PPM."""
    update_email_signature()
