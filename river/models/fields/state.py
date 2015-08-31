from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation

from river.models import State, Approvement
from river.models.approvement_track import ApprovementTrack
from river.models.managers.wofkflow_object import WorkflowObjectManager
from river.services.object import ObjectService
from river.services.transition import TransitionService

__author__ = 'ahmetdal'

from django.db import models


class StateField(models.ForeignKey):
    def __init__(self, state_model=State, object_manager=WorkflowObjectManager, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        self.object_manager = object_manager
        kwargs['to'] = '%s.%s' % (state_model._meta.app_label, state_model._meta.object_name)
        super(StateField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        def is_workflow_completed(workflow_object):
            return ObjectService.is_workflow_completed(workflow_object, name)

        def approve(self, user, *args, **kwargs):
            TransitionService.approve_transition(self, name, user, *args, **kwargs)

        def reject(self, user, *args, **kwargs):
            TransitionService.reject_transition(self, name, user, *args, **kwargs)

        @property
        def on_initial_state(self):
            from river.services.state import StateService

            return StateService.get_initial_state(ContentType.objects.get_for_model(self), name) == getattr(self, name)

        @property
        def on_final_state(self):
            from river.services.state import StateService

            return getattr(self, name) in StateService.get_final_states(ContentType.objects.get_for_model(self), name)

        def get_initial_state(self):
            from river.services.state import StateService

            return StateService.get_initial_state(ContentType.objects.get_for_model(self), name)

        def get_available_approvements(self, *args, **kwargs):
            from river.services.approvement import ApprovementService

            return ApprovementService.get_approvements_object_waiting_for_approval(self, name, [getattr(self, name)], *args, **kwargs)

        @property
        def initial_approvements(self):
            from river.services.approvement import ApprovementService

            return getattr(self, name) in ApprovementService.get_initial_approvements(ContentType.objects.get_for_model(self), name)

        @property
        def final_approvements(self):
            from river.services.approvement import ApprovementService

            return getattr(self, name) in ApprovementService.get_final_approvements(ContentType.objects.get_for_model(self), name)

        @property
        def next_approvements(self):
            from river.services.approvement import ApprovementService

            return getattr(self, name) in ApprovementService.get_next_approvements(ContentType.objects.get_for_model(self), name)

        self.model = cls

        self.__add_to_class(cls, "approvements", GenericRelation('%s.%s' % (Approvement._meta.app_label, Approvement._meta.object_name)))
        self.__add_to_class(cls, "approvement_track", models.ForeignKey('%s.%s' % (ApprovementTrack._meta.app_label, ApprovementTrack._meta.object_name), null=True, blank=True))

        self.__add_to_class(cls, "objects", self.object_manager(name))
        self.__add_to_class(cls, "is_workflow_completed", is_workflow_completed)
        self.__add_to_class(cls, "approve", approve)
        self.__add_to_class(cls, "reject", reject)

        self.__add_to_class(cls, "on_initial_state", on_initial_state)
        self.__add_to_class(cls, "on_final_state", on_final_state)

        self.__add_to_class(cls, "get_initial_state", get_initial_state)
        self.__add_to_class(cls, "get_available_approvements", get_available_approvements)

        self.__add_to_class(cls, "initial_approvements", initial_approvements)
        self.__add_to_class(cls, "final_approvements", final_approvements)
        self.__add_to_class(cls, "next_approvements", next_approvements)

        super(StateField, self).contribute_to_class(cls, name, virtual_only=virtual_only)

        post_save.connect(_post_save, self.model, False, dispatch_uid='%s_%s_riverstatefield_post' % (self.model, self.name))
        # self.model.__metaclass__ = WorkflowObjectMetaclass

    def get_state(self, instance):
        return instance.__dict__[self.attname]

    def set_state(self, instance, state):
        instance.__dict__[self.attname] = state.pk

    def __add_to_class(self, cls, key, value):
        if not hasattr(cls, key):
            cls.add_to_class(key, value)


def _post_save(sender, instance, created, *args, **kwargs):  # signal, sender, instance):
    """
    Desc:  Generate TransitionApprovements according to TransitionApproverDefinition of the content type at the beginning.
    :param kwargs:
    :return:
    """

    if created:
        for f in instance._meta.fields:
            if isinstance(f, StateField):
                ObjectService.register_object(instance, f.name)
