from uuid import uuid4

from .base import *

DB_HOST = os.environ['MYSQL_HOST']
DB_PORT = os.environ['MYSQL_3306_TCP_PORT']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'river',
        'USER': 'root',
        'PASSWORD': 'river',
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'TEST': {
            'NAME': 'river' + str(uuid4()),
        },
    }
}

INSTALLED_APPS += (
    'river.tests',
)

if django.get_version() >= '1.9.0':
    MIGRATION_MODULES = DisableMigrations()
