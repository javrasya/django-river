import logging
from abc import abstractmethod

from river.hooking.backends.loader import callback_backend

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class Hooking(object):

    @staticmethod
    def get_result_exclusions():
        return []

    @classmethod
    def dispatch(cls, workflow_object, field_name, *args, **kwargs):
        LOGGER.debug("Hooking %s is dispatched for workflow object %s and field name %s" % (cls.__name__, workflow_object, field_name))
        kwargs.pop('signal', None)
        kwargs.pop('sender', None)

        for callback in callback_backend.get_callbacks(cls, workflow_object, field_name, *args, **kwargs):
            exclusions = cls.get_result_exclusions()
            callback(workflow_object, field_name, *args, **{k: v for k, v in kwargs.items() if k not in exclusions})
            LOGGER.debug(
                "Hooking %s for workflow object %s and for field %s is found as method %s with args %s and kwargs %s" % (cls.__name__, workflow_object, field_name, callback.__name__, args, kwargs))

    @classmethod
    def register(cls, callback, workflow_object, field_name, override=False, *args, **kwargs):
        callback_backend.register(cls, callback, workflow_object, field_name, override, *args, **kwargs)

    @classmethod
    def get_hash(cls, workflow_object, field_name, *args, **kwargs):
        return 'object' + (str(workflow_object.pk) if workflow_object else '') + '_field_name' + field_name
