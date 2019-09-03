from django.contrib import admin

from river.admin.transitionapprovalmeta import TransitionApprovalMetaAdmin
from river.admin.workflow import WorkflowAdmin
from river.models import State

admin.site.register(State)
