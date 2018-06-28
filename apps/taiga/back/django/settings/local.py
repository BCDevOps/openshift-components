from .common import *
import os

try:
    from .logging import *
except ImportError:
    pass

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

# disable public registration by default
PUBLIC_REGISTER_ENABLED = os.environ.get('TAIGA_PUBLIC_REGISTER_ENABLED', False)

if os.environ.get('TAIGA_GITHUB_AUTH_ENABLED', False):
    # requirements for github-auth plugin
    INSTALLED_APPS += ["taiga_contrib_github_auth", "taiga.taiga_contrib_github_extended_auth"]

    # Get these from https://github.com/settings/developers
    GITHUB_API_CLIENT_ID = os.environ.get('GITHUB_API_CLIENT_ID', '')
    GITHUB_API_CLIENT_SECRET = os.environ.get('GITHUB_API_CLIENT_SECRET', '')

    TAIGA_GITHUB_EXTENDED_AUTH_ORG = os.environ.get('TAIGA_GITHUB_EXTENDED_AUTH_ORG', None)

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

IMPORTERS["github"] = {
   "active": True, # Enable or disable the importer
   "client_id": os.environ.get('GITHUB_API_CLIENT_ID', ''),
   "client_secret": os.environ.get('GITHUB_API_CLIENT_SECRET', '')
}