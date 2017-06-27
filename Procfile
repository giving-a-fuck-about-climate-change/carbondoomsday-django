uwsgi: uwsgi --emperor uwsgi.ini
web: daphne carbondoomsday.asgi:channel_layer --port $PORT --bind 0.0.0.0 --verbosity 2
celerybeatworker: celery --app=carbondoomsday --loglevel=INFO worker --beat --task-events
channelsworker: python manage.py runworker --verbosity 2
