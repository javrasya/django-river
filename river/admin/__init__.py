from django.contrib import admin

from river.admin.proceeding_meta import ProceedingMetaAdmin
from river.models import State, Transition

admin.site.register(State)
admin.site.register(Transition)

import proceeding_meta
