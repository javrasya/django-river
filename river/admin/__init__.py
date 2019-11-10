from django.contrib import admin

from river.admin.function_admin import *
from river.admin.transitionmeta import *
from river.admin.transitionapprovalmeta import *
from river.admin.workflow import *
from river.admin.hook_admins import *
from river.models import State

admin.site.register(State)
