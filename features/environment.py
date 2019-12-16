import os

import django
from behave import register_type
from django.core import management

os.environ["DJANGO_SETTINGS_MODULE"] = "settings.with_sqlite3"


def before_all(context):
    django.setup()


def before_scenario(context, scenario):
    management.call_command('flush', interactive=False)


def parse_string_with_whitespace(text):
    return text


def parse_list(text):
    return [better_item.strip() for item in text.split(" or ") for better_item in item.split(" and ")]


# -- REGISTER: User-defined type converter (parse_type).
register_type(ws=parse_string_with_whitespace)
register_type(list=parse_list)
