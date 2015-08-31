import logging
from river.handlers.backends.base import BaseHandlerBackend, powerset

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class MemoryHandlerBackend(BaseHandlerBackend):
    def __init__(self):
        self.handlers = {}

    def register(self, handler_cls, handler, workflow_object, field, override=False, *args, **kwargs):
        hash = self.get_handler_class_prefix(handler_cls) + handler_cls.get_hash(workflow_object, field, *args, **kwargs)
        if override or hash not in self.handlers:
            self.handlers[hash] = handler
            LOGGER.debug("Handler '%s'  is registered in memory as method '%s' and module '%s'. " % (hash, handler.__name__, handler.__module__))
        return hash

    def get_handlers(self, handler_cls, workflow_object, field, *args, **kwargs):
        handlers = []
        for c in powerset(kwargs.keys()):
            skwargs = {}
            for f in c:
                skwargs[f] = kwargs.get(f)
            hash = self.get_handler_class(handler_cls).get_hash(workflow_object, field, **skwargs)
            handler = self.handlers.get(self.get_handler_class_prefix(self.get_handler_class(handler_cls)) + hash)
            if handler:
                handlers.append(handler)
        return handlers
