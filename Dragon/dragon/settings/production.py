import os
from .base import *
import sentry_sdk


DEBUG = False
SECRET_KEY = 'django-insecure-ufsnyywvlk+d-1rkt+3eeb8&em=o&=_58t2$_^)@1h!p3m(6a#mdf8pc^5cou1p2u@j9fx0u&pkv9s-t(eb$u_vq=as350womo%='
ALLOWED_HOSTS = ['localhost', 'dragon.kaido.to', ''] # remove IP once you launch the website

cwd = os.getcwd()

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": f"{cwd}/.cache"
    }
}

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'dragon',
        "USER": 'dragon',
        "PASSWORD": 'cosmic!1x',
        "HOST": 'localhost',
        "PORT": "",
    }
}

sentry_sdk.init(
    dsn="https://d9e30f8a1f0976c79c02de9b2103bc53@o4507199015092224.ingest.us.sentry.io/4507199019417600",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

try:
    from .local import *
except ImportError:
    pass
