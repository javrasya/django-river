import logging

from river.hooking.backends.loader import callback_backend

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class Hooking(object):
    @classmethod
    def dispatch(cls, workflow_object, field_name, *args, **kwargs):
        LOGGER.debug("Hooking %s is dispatched for workflow object %s" % (cls.__name__, workflow_object))
        kwargs.pop('signal', None)
        kwargs.pop('sender', None)

        for callback in callback_backend.get_callbacks(cls, workflow_object, field_name, *args, **kwargs):
            callback(workflow_object, field_name, *args, **kwargs)
            LOGGER.debug(
                "Hooking %s for workflow object %s and for field %s is found as method %s with args %s and kwargs %s" % (cls.__name__, workflow_object, field_name, callback.__name__, args, kwargs))

    @classmethod
    def register(cls, callback, workflow_object, field_name, override=False, *args, **kwargs):
        callback_backend.register(cls, callback, workflow_object, field_name, override, *args, **kwargs)

    @classmethod
    def get_hash(cls, workflow_object, field_name, *args, **kwargs):
        return 'object' + (str(workflow_object.pk) if workflow_object else '') + '_field_name' + field_name
