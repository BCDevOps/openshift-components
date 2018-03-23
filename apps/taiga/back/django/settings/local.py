from .common import *
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taiga',
        'USER': 'taiga',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_SERVICE_NAME', ''),
        'PORT': '5432',
    }
}

MEDIA_URL = os.environ.get('TAIGA_MEDIA_URL', '')
STATIC_URL = os.environ.get('TAIGA_STATIC_URL', '')
SITES["front"]["scheme"] = os.environ.get('TAIGA_FRONT_SCHEME', '')
SITES["front"]["domain"] = os.environ.get('TAIGA_FRONT_DOMAIN', '')

DEBUG = False
PUBLIC_REGISTER_ENABLED = True

DEFAULT_FROM_EMAIL = os.environ.get('TAIGA_FROM_EMAIL_ADDRESS', 'no-reply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

#CELERY_ENABLED = True

# EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
# EVENTS_PUSH_BACKEND_OPTIONS = {"url": "amqp://taiga:PASSWORD_FOR_EVENTS@localhost:5672/taiga"}

# Uncomment and populate with proper connection parameters
# for enable email sending. EMAIL_HOST_USER should end by @domain.tld
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = os.environ.get('TAIGA_EMAIL_HOST','')
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 25

# requirements for github-auth plugin

INSTALLED_APPS += ["taiga_contrib_github_auth"]

# Get these from https://github.com/settings/developers
GITHUB_API_CLIENT_ID = os.environ.get('GITHUB_API_CLIENT_ID', '')
GITHUB_API_CLIENT_SECRET = os.environ.get('GITHUB_API_CLIENT_SECRET', '')


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "formatters": {
        "complete": {
            "format": "%(levelname)s:%(asctime)s:%(module)s %(message)s"
        },
        "simple": {
            "format": "%(levelname)s:%(asctime)s: %(message)s"
        },
        "null": {
            "format": "%(message)s",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        },
    },
    "handlers": {
        "null": {
            "level":"DEBUG",
            "class":"logging.NullHandler",
        },
        "console":{
            "level":"DEBUG",
            "class":"logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django": {
            "handlers":["null"],
            "propagate": True,
            "level":"INFO",
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "taiga.export_import": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "taiga": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        }
    }
}
