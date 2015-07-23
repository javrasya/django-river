from django.contrib.contenttypes.fields import GenericRelation
from river.models import State, Approvement
from river.models.meta.workflow_object import WorkflowObjectMetaclass

__author__ = 'ahmetdal'

from django.db import models


class StateField(models.ForeignKey):
    def __init__(self, state_model=State, reverse_identifier=None, *args, **kwargs):
        kwargs.pop('to', None)
        kwargs['null'] = True
        kwargs['blank'] = True
        self.reverse_identifier = reverse_identifier
        super(StateField, self).__init__(state_model, *args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        self.model = cls

        approvements_field = GenericRelation(Approvement, related_query_name=self.reverse_identifier)
        cls.add_to_class("approvements", approvements_field)

        super(StateField, self).contribute_to_class(cls, name, virtual_only=virtual_only)
        self.model.__metaclass__ = WorkflowObjectMetaclass

    def get_state(self, instance):
        return instance.__dict__[self.attname]

    def set_state(self, instance, state):
        instance.__dict__[self.attname] = state.pk
