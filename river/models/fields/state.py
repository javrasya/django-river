import logging

from django.db.models import CASCADE
from django.db.models.signals import post_save, post_delete

from river.core.riverobject import RiverObject
from river.core.workflowregistry import workflow_registry
from river.hooking.completed import PreCompletedHooking, PostCompletedHooking
from river.hooking.transition import PostTransitionHooking, PreTransitionHooking

try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation

from river.models.state import State
from river.models.transitionapproval import TransitionApproval

__author__ = 'ahmetdal'

from django.db import models

LOGGER = logging.getLogger(__name__)


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(instance) if instance else self.getter(owner)


class StateField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        self.field_name = None
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['to'] = '%s.%s' % (State._meta.app_label, State._meta.object_name)
        kwargs['on_delete'] = kwargs.get('on_delete', CASCADE)
        kwargs['related_name'] = "+"
        super(StateField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        @classproperty
        def river(_self):
            return RiverObject(_self, name)

        self.field_name = name

        self._add_to_class(cls, self.field_name + "_transitions", GenericRelation('%s.%s' % (TransitionApproval._meta.app_label, TransitionApproval._meta.object_name)))

        if id(cls) not in workflow_registry.workflows:
            self._add_to_class(cls, "river", river)

        super(StateField, self).contribute_to_class(cls, name)

        if id(cls) not in workflow_registry.workflows:
            post_save.connect(_on_workflow_object_saved, self.model, False, dispatch_uid='%s_%s_riverstatefield_post' % (self.model, name))
            post_delete.connect(_on_workflow_object_deleted, self.model, False, dispatch_uid='%s_%s_riverstatefield_post' % (self.model, name))

        workflow_registry.add(self.field_name, cls)

    @staticmethod
    def _add_to_class(cls, key, value, ignore_exists=False):
        if ignore_exists or not hasattr(cls, key):
            cls.add_to_class(key, value)


def _on_workflow_object_saved(sender, instance, created, *args, **kwargs):
    for instance_workflow in instance.river.all(instance.__class__):
        if created:
            instance_workflow.initialize_approvals()
        if not instance_workflow.get_state():
            init_state = getattr(instance.__class__.river, instance_workflow.name).initial_state
            instance_workflow.set_state(init_state)
            instance.save()


def _on_workflow_object_deleted(sender, instance, *args, **kwargs):
    for field_name in instance.river.all_field_names(instance.__class__):
        PreCompletedHooking.unregister(instance, field_name, *args, **kwargs)
        PostCompletedHooking.unregister(instance, field_name, *args, **kwargs)
        PreTransitionHooking.unregister(instance, field_name, *args, **kwargs)
        PostTransitionHooking.unregister(instance, field_name, *args, **kwargs)
