import sys
import os

__author__ = 'ahmetdal'
BASE_DIR = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'river',
    'river.tests'
)

SITE_ID = 1

SECRET_KEY = 'abcde12345'

ROOT_URLCONF = 'test_urls'
