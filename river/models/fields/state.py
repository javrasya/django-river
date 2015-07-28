from django.contrib.contenttypes.fields import GenericRelation

from river.models import State, Approvement
from river.models.managers.wofkflow_object import WorkflowObjectManager
from river.models.meta.workflow_object import WorkflowObjectMetaclass
from river.services.object import ObjectService

__author__ = 'ahmetdal'

from django.db import models


class StateField(models.ForeignKey):
    def __init__(self, state_model=State, reverse_identifier=None, object_manager=WorkflowObjectManager, *args, **kwargs):
        kwargs.pop('to', None)
        kwargs['null'] = True
        kwargs['blank'] = True
        self.reverse_identifier = reverse_identifier
        self.object_manager = object_manager
        super(StateField, self).__init__(state_model, *args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        def is_workflow_completed(workflow_object):
            return ObjectService.is_workflow_completed(workflow_object, name)

        self.model = cls

        approvements_field = GenericRelation(Approvement, related_query_name=self.reverse_identifier)
        cls.add_to_class("approvements", approvements_field)
        cls.add_to_class("objects", self.object_manager(name))
        cls.add_to_class("is_workflow_completed", is_workflow_completed)

        super(StateField, self).contribute_to_class(cls, name, virtual_only=virtual_only)
        self.model.__metaclass__ = WorkflowObjectMetaclass

    def get_state(self, instance):
        return instance.__dict__[self.attname]

    def set_state(self, instance, state):
        instance.__dict__[self.attname] = state.pk
