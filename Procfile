release: python manage.py migrate --no-input
web: uwsgi --emperor uwsgi.ini
celerybeatworker: celery --app=carbondoomsday --loglevel=INFO worker --beat --task-events
