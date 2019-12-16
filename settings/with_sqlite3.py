from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

INSTALLED_APPS += (
    'river.tests',
)

if django.get_version() >= '1.9.0':
    MIGRATION_MODULES = DisableMigrations()
