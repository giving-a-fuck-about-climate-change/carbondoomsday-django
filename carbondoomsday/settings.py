"""Project settings."""

import os
from datetime import timedelta

import dj_database_url
from configurations import Configuration, values


class Base(Configuration):
    """The base configuration for each environment."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    PROJECT = 'carbondoomsday'

    SCHEMA_TITLE = 'CarbonDoomsDay Web API'

    DEBUG = values.BooleanValue(False)

    WSGI_APPLICATION = 'carbondoomsday.wsgi.application'

    ROOT_URLCONF = 'carbondoomsday.urls'

    WSGI_APPLICATION = 'carbondoomsday.wsgi.application'

    DATABASES = {'default': dj_database_url.config()}
    DATABASES['default']['CONN_MAX_AGE'] = 500

    SECRET_KEY = values.SecretValue()

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'carbondoomsday.measurements',
        'django_extensions',
        'django_filters',
        'rest_framework',
        'rest_framework_swagger',
        'opbeat.contrib.django',
        'corsheaders',
        'channels',
    )

    MIDDLEWARE_CLASSES = (
        'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'carbondoomsday': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

    CELERY_BROKER_URL = values.Value()
    CELERY_RESULT_BACKEND = values.Value()

    LATEST_CO2_URL = (
        'https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2_mlo_weekly.csv'
    )

    HISTORIC_CO2_URL = (
        'ftp://aftp.cmdl.noaa.gov/data/trace_gases/co2/in-situ/'
        'surface/mlo/co2_mlo_surface-insitu_1_ccgg_DailyData.txt'
    )

    REST_FRAMEWORK = {
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework_filters.backends.DjangoFilterBackend',
            'rest_framework.filters.OrderingFilter',
        ),
        'DEFAULT_PAGINATION_CLASS': (
            'rest_framework.pagination.LimitOffsetPagination'
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'PAGE_SIZE': 50,
    }

    SWAGGER_SETTINGS = {
        'APIS_SORTER': 'alpha',
        'DOC_EXPANSION': 'list',
        'JSON_EDITOR': True,
        'SHOW_REQUEST_HEADERS': True,
    }

    CELERY_BEAT_SCHEDULE = {
        'scrape-latest-co2-measurements-from-MLO': {
            'task': 'carbondoomsday.measurements.tasks.scrape_latest_co2',
            'schedule': timedelta(hours=6)
        }
    }


class ChannelsWithRedis():
    """Channels production settings."""
    REDIS_URL = values.Value(environ_name='REDIS_URL')
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'asgi_redis.RedisChannelLayer',
            'ROUTING': 'carbondoomsday.routing.appchannels',
            'CONFIG': {'hosts': [REDIS_URL]},
        },
    }


class OpbeatCredentials():
    """Opbeat communication credentials."""
    OPBEAT_APP_ID = values.Value()
    OPBEAT_ORGANIZATION_ID = values.Value()
    OPBEAT_SECRET_TOKEN = values.SecretValue()
    OPBEAT = {
        'APP_ID': OPBEAT_APP_ID,
        'ORGANIZATION_ID': OPBEAT_ORGANIZATION_ID,
        'SECRET_TOKEN': OPBEAT_SECRET_TOKEN,
    }


class Production(ChannelsWithRedis, OpbeatCredentials, Base):
    """The production environment."""
    ENVIRONMENT = 'Production'
    ALLOWED_HOSTS = [
        'carbondoomsday.herokuapp.com',
        'api.carbondoomsday.com',
    ]


class Staging(ChannelsWithRedis, OpbeatCredentials, Base):
    """The staging environment."""
    ENVIRONMENT = 'Staging'
    ALLOWED_HOSTS = [
        'carbondoomsday-test.herokuapp.com'
    ]


class Development(Base):
    """The development environment."""
    ENVIRONMENT = 'Development'
    DEBUG = values.BooleanValue(True)
    CELERY_TASK_ALWAYS_EAGER = values.BooleanValue(True)
    OPBEAT_DISABLE_SEND = values.BooleanValue(True)
    CORS_ORIGIN_ALLOW_ALL = values.BooleanValue(True)
    CORS_ALLOW_CREDENTIALS = values.BooleanValue(False)

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'asgiref.inmemory.ChannelLayer',
            'ROUTING': 'carbondoomsday.routing.appchannels',
        },
    }
