import subprocess
from time import sleep
from uuid import uuid4

from .base import *

DB_HOST = os.environ['MYSQL_HOST']
DB_PORT = os.environ['MYSQL_3306_TCP_PORT']


def get_container_id():
    lines = subprocess.check_output(
        "docker ps --format \"{{.ID}},{{.Ports}}\" | grep '%s:%s' | awk -F',' '{print $1}'" % (DB_HOST, DB_PORT)
        , shell=True
    ).decode("utf-8").splitlines()
    return next(iter(lines), None)


def wait_for_container_to_be_up():
    container_id = get_container_id()
    while True:
        logs = subprocess.check_output("docker logs %s" % container_id, shell=True).decode("utf-8")
        if "MySQL init process done. Ready for start up" in logs:
            break
        sleep(3)
        print("Waiting DB to be up an running...")
    print("DB is ready!")


wait_for_container_to_be_up()

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
