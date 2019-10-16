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

    def _register_hook_inlines(self, model):
        from django.contrib import admin
        from django.contrib.contenttypes.admin import GenericTabularInline

        from river.models import OnApprovedHook, OnTransitHook, OnCompleteHook
        _get_workflow_class_fields = self._get_workflow_class_fields

        class BaseHookInline(GenericTabularInline):
            fields = ("callback_function", "hook_type")

        class OnApprovedHookInline(BaseHookInline):
            model = OnApprovedHook

            def __init__(self, *args, **kwargs):
                super(OnApprovedHookInline, self).__init__(*args, **kwargs)
                self.fields += ("transition_approval_meta",)

        class OnTransitHookInline(BaseHookInline):
            model = OnTransitHook

            def __init__(self, *args, **kwargs):
                super(OnTransitHookInline, self).__init__(*args, **kwargs)
                self.fields += ("source_state", "destination_state",)

        class OnCompleteHookInline(BaseHookInline):
            model = OnCompleteHook

        class DefaultWorkflowModelAdmin(admin.ModelAdmin):
            inlines = [
                OnApprovedHookInline,
                OnTransitHookInline,
                OnCompleteHookInline
            ]

            def __init__(self, *args, **kwargs):
                super(DefaultWorkflowModelAdmin, self).__init__(*args, **kwargs)
                self.readonly_fields += tuple(_get_workflow_class_fields(model))

        registered_admin = admin.site._registry.get(model, None)
        if registered_admin:
            if OnApprovedHookInline not in registered_admin.inlines:
                registered_admin.inlines.append(OnApprovedHookInline)
                registered_admin.inlines.append(OnTransitHookInline)
                registered_admin.inlines.append(OnCompleteHookInline)
                registered_admin.readonly_fields = list(set(list(registered_admin.readonly_fields) + list(_get_workflow_class_fields(model))))
                admin.site._registry[model] = registered_admin
        else:
            admin.site.register(model, DefaultWorkflowModelAdmin)



def handle(context):
    print(datetime.now())
    print(context)