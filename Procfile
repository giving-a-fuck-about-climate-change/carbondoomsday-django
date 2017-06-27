web: uwsgi --emperor uwsgi.ini
webchannels: daphne carbondoomsday.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
celerybeatworker: celery --app=carbondoomsday --loglevel=INFO worker --beat --task-events
channelsworker: python manage.py runworker --verbosity 2
