import logging

from river.handlers.backends.loader import handler_backend

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class Handler(object):
    @classmethod
    def dispatch(cls, workflow_object, field, *args, **kwargs):
        LOGGER.debug("Handler %s is dispatched for workflow object %s for field %s" % (cls.__name__, workflow_object, field))
        kwargs.pop('signal', None)
        kwargs.pop('sender', None)

        for handler in handler_backend.get_handlers(cls, workflow_object, field, *args, **kwargs):
            handler(workflow_object, field, *args, **kwargs)
            LOGGER.debug("Handler %s for workflow object %s for field %s is found as method %s with args %s and kwargs %s" % (cls.__name__, workflow_object, field, handler.__name__, args, kwargs))

    @classmethod
    def register(cls, handler, workflow_object, field, override=False, *args, **kwargs):
        handler_backend.register(cls, handler, workflow_object, field, override, *args, **kwargs)

    @classmethod
    def get_hash(cls, workflow_object, field, *args, **kwargs):
        return 'object' + (str(workflow_object.pk) if workflow_object else '') + 'field' + (field or '')
