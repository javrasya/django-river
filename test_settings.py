import os
import sys

import django

__author__ = 'ahmetdal'
BASE_DIR = os.path.dirname(__file__)

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST_NAME': os.path.join(BASE_DIR, 'db.test.sqlite3'),
    },
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'river',  # Or path to database file if using sqlite3.
#         # The following settings are not used with sqlite3:
#         'USER': 'river',
#         'PASSWORD': 'q1w2e3r4',
#         'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '5432',  # Set to empty string for default.1
#     }
# }


USE_TZ = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'river',
)


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


TESTING = any("py.test" in s for s in sys.argv) or 'test' in sys.argv
if TESTING:
    INSTALLED_APPS += (
        'river.tests',
    )

    if django.get_version() >= '1.9.0':
        MIGRATION_MODULES = DisableMigrations()

SITE_ID = 1

SECRET_KEY = 'abcde12345'

ROOT_URLCONF = 'test_urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '(%(module)s) (%(name)s) (%(asctime)s) (%(levelname)s) %(message)s',
            'datefmt': "%Y-%b-%d %H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }

    },
    'loggers': {
        'river': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}
