import logging
from uuid import uuid4

from django.db.models import CASCADE
from django.db.models.signals import post_save

from river.core.riverobject import RiverObject
from river.core.workflowregistry import workflow_registry

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
        kwargs['related_name'] = "rn" + str(uuid4()).replace("-", "")
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
            post_save.connect(_post_save, self.model, False, dispatch_uid='%s_%s_riverstatefield_post' % (self.model, name))

        workflow_registry.add(self.field_name, cls)


    @staticmethod
    def _add_to_class(cls, key, value, ignore_exists=False):
        if ignore_exists or not hasattr(cls, key):
            cls.add_to_class(key, value)


def _post_save(sender, instance, created, *args, **kwargs):  # signal, sender, instance):
    for workflow in instance.river.all(instance.__class__):
        if created:
            workflow.initialize_approvals()
        if not workflow.get_state():
            init_state = getattr(instance.__class__.river, workflow.name).initial_state
            workflow.set_state(init_state)
            instance.save()
