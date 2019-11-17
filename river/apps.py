import logging
import operator
from functools import reduce

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

LOGGER = logging.getLogger(__name__)


class RiverApp(AppConfig):
    name = 'river'
    label = 'river'

    def ready(self):

        for field_name in self._get_all_workflow_fields():
            try:
                workflows = self.get_model('Workflow').objects.filter(field_name=field_name)
                if workflows.count() == 0:
                    LOGGER.warning("%s field doesn't seem have any workflow defined in database. You should create its workflow" % field_name)
            except (OperationalError, ProgrammingError):
                pass

        from river.config import app_config

        if app_config.INJECT_MODEL_ADMIN:
            for model_class in self._get_all_workflow_classes():
                self._register_hook_inlines(model_class)

        LOGGER.debug('RiverApp is loaded.')

    @classmethod
    def _get_all_workflow_fields(cls):
        from river.core.workflowregistry import workflow_registry
        return reduce(operator.concat, map(list, workflow_registry.workflows.values()), [])

    @classmethod
    def _get_all_workflow_classes(cls):
        from river.core.workflowregistry import workflow_registry
        return list(workflow_registry.class_index.values())

    @classmethod
    def _get_workflow_class_fields(cls, model):
        from river.core.workflowregistry import workflow_registry
        return workflow_registry.workflows[id(model)]

    def _register_hook_inlines(self, model):  # pylint: disable=no-self-use
        from django.contrib import admin
        from river.core.workflowregistry import workflow_registry
        from river.admin import OnApprovedHookInline, OnTransitHookInline, OnCompleteHookInline, DefaultWorkflowModelAdmin

        registered_admin = admin.site._registry.get(model, None)
        if registered_admin:
            if OnApprovedHookInline not in registered_admin.inlines:
                registered_admin.inlines = list(set(registered_admin.inlines + [OnApprovedHookInline, OnTransitHookInline, OnCompleteHookInline]))
                registered_admin.readonly_fields = list(set(list(registered_admin.readonly_fields) + list(workflow_registry.get_class_fields(model))))
                admin.site._registry[model] = registered_admin
        else:
            admin.site.register(model, DefaultWorkflowModelAdmin)
