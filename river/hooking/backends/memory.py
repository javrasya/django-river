import logging
from river.hooking.backends.base import BaseHookingBackend, powerset

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class MemoryHookingBackend(BaseHookingBackend):
    def __init__(self):
        self.callbacks = {}

    def register(self, hooking_cls, callback, workflow_object, field_name, override=False, *args, **kwargs):
        hash = self.get_hooking_class_prefix(hooking_cls) + hooking_cls.get_hash(workflow_object, field_name, *args, **kwargs)
        if override or hash not in self.callbacks:
            self.callbacks[hash] = callback
            LOGGER.debug("Callback '%s'  is registered in memory as method '%s' and module '%s'. " % (hash, callback.__name__, callback.__module__))
        return hash

    def get_callbacks(self, hooking_cls, workflow_object, field_name, *args, **kwargs):
        callabacks = []
        for c in powerset(kwargs.keys()):
            skwargs = {}
            for f in c:
                skwargs[f] = kwargs.get(f)
            hash = self.get_hooking_class(hooking_cls).get_hash(workflow_object, field_name, **skwargs)
            callback = self.callbacks.get(self.get_hooking_class_prefix(self.get_hooking_class(hooking_cls)) + hash)
            if callback:
                callabacks.append(callback)
        return callabacks
