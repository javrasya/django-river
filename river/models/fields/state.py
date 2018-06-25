from django.contrib.contenttypes.models import ContentType
from django.db.models import CASCADE
from django.db.models.signals import post_save

from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation

from river.models.state import State
from river.models.proceeding import Proceeding
from river.services.object import ObjectService
from river.services.transition import TransitionService

__author__ = 'ahmetdal'

from django.db import models

class_field_rl = {}


def _get_cls_identifier(cls):
    return cls.__module__ + "." + cls.__name__


def _get_identifier(cls_identifier, field):
    return "%s_%s" % (cls_identifier, field)


class StateField(models.ForeignKey):
    def __init__(self, state_model=State, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['to'] = '%s.%s' % (state_model._meta.app_label, state_model._meta.object_name)
        kwargs['on_delete'] = kwargs.get('on_delete', CASCADE)
        super(StateField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        def is_workflow_completed(workflow_object):
            return ObjectService.is_workflow_completed(workflow_object)

        def proceed(self, user, *args, **kwargs):
            TransitionService.proceed(self, user, *args, **kwargs)

        @property
        def on_initial_state(self):
            from river.services.state import StateService

            return StateService.get_initial_state(ContentType.objects.get_for_model(self)) == self.get_state()

        @property
        def on_final_state(self):
            from river.services.state import StateService

            return self.get_state() in StateService.get_final_states(ContentType.objects.get_for_model(self))

        def get_initial_state(self):
            from river.services.state import StateService

            return StateService.get_initial_state(ContentType.objects.get_for_model(self))

        def get_available_proceedings(self, *args, **kwargs):
            from river.services.proceeding import ProceedingService

            return ProceedingService.get_available_proceedings(self, [self.get_state()], *args, **kwargs)

        @property
        def initial_proceedings(self):
            from river.services.proceeding import ProceedingService

            return self.get_state() in ProceedingService.get_initial_proceedings(ContentType.objects.get_for_model(self))

        @property
        def final_proceedings(self):
            from river.services.proceeding import ProceedingService

            return self.get_state() in ProceedingService.get_final_proceedings(ContentType.objects.get_for_model(self))

        @property
        def next_proceedings(self):
            from river.services.proceeding import ProceedingService

            return self.get_state() in ProceedingService.get_next_proceedings(ContentType.objects.get_for_model(self))

        @property
        def proceeding(self):
            try:
                return self.proceedings.filter(transaction_date__isnull=False).latest('transaction_date')
            except Proceeding.DoesNotExist:
                return None

        def _get_state(self):
            return getattr(self, name)

        def _set_state(self, state):
            setattr(self, name, state)

        field_identifiers = [_get_identifier(c, f) for c, f in class_field_rl.items()]
        cls_identifier = _get_cls_identifier(cls)
        field_identifier = _get_identifier(cls_identifier, name)
        if field_identifier not in field_identifiers:

            if cls_identifier in class_field_rl.keys():
                raise RiverException(ErrorCode.MULTIPLE_STATE_FIELDS,
                                     "There can be only one state field in a model class. Class:%s - Field:%s." % (cls.__name__, name))

            class_field_rl[cls_identifier] = name

        self.model = cls
        self.__add_to_class(cls, "proceedings", GenericRelation('%s.%s' % (Proceeding._meta.app_label, Proceeding._meta.object_name)))
        self.__add_to_class(cls, "proceeding", proceeding)

        self.__add_to_class(cls, "is_workflow_completed", is_workflow_completed)
        self.__add_to_class(cls, "proceed", proceed)

        self.__add_to_class(cls, "on_initial_state", on_initial_state)
        self.__add_to_class(cls, "on_final_state", on_final_state)

        self.__add_to_class(cls, "get_initial_state", get_initial_state)
        self.__add_to_class(cls, "get_available_proceedings", get_available_proceedings)

        self.__add_to_class(cls, "initial_proceedings", initial_proceedings)
        self.__add_to_class(cls, "final_proceedings", final_proceedings)
        self.__add_to_class(cls, "next_proceedings", next_proceedings)

        self.__add_to_class(cls, "get_state", _get_state)
        self.__add_to_class(cls, "set_state", _set_state)

        super(StateField, self).contribute_to_class(cls, name)

        post_save.connect(_post_save, self.model, False, dispatch_uid='%s_%s_riverstatefield_post' % (self.model, name))

    def __add_to_class(self, cls, key, value):
        if not hasattr(cls, key):
            cls.add_to_class(key, value)


def _post_save(sender, instance, created, *args, **kwargs):  # signal, sender, instance):
    """
    Desc:  Generate TransitionProceedings according to ProceedingMeta of the content type at the beginning.
    :param kwargs:
    :return:
    """
    from river.services.state import StateService

    if created:
        ObjectService.register_object(instance)
    if not instance.get_state():
        init_state = StateService.get_initial_state(ContentType.objects.get_for_model(instance))
        instance.set_state(init_state)
        instance.save()
