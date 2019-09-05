import logging
from river.hooking.backends.base import BaseHookingBackend, powerset

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class MemoryHookingBackend(BaseHookingBackend):
    def __init__(self):
        self.callbacks = {}

    def register(self, hooking_cls, callback, workflow_object, field_name, override=False, *args, **kwargs):
        callback_hash = self.get_hooking_class_prefix(hooking_cls) + hooking_cls.get_hash(workflow_object, field_name, *args, **kwargs)
        if override or callback_hash not in self.callbacks:
            self.callbacks[callback_hash] = callback
            LOGGER.debug("Callback '%s'with method '%s' and module '%s'  is registered from memory" % (callback_hash, callback.__name__, callback.__module__))
        return callback_hash

    def unregister(self, hooking_cls, workflow_object, field_name, *args, **kwargs):
        callback_hash = self.get_hooking_class_prefix(hooking_cls) + hooking_cls.get_hash(workflow_object, field_name, *args, **kwargs)

        if callback_hash in self.callbacks:
            callback_method = self.callbacks.pop(callback_hash)
            LOGGER.debug("Callback '%s'with method '%s' and module '%s'  is unregistered from memory. " % (callback_hash, callback_method.__name__, callback_method.__module__))
            return callback_hash, callback_method
        else:
            return None, None

    def get_callbacks(self, hooking_cls, workflow_object, field_name, *args, **kwargs):
        callbacks = []
        for c in powerset(kwargs.keys()):
            skwargs = {}
            for f in c:
                skwargs[f] = kwargs.get(f)
            callback_hash = self.get_hooking_class(hooking_cls).get_hash(workflow_object, field_name, **skwargs)
            callback = self.callbacks.get(self.get_hooking_class_prefix(self.get_hooking_class(hooking_cls)) + callback_hash)
            if callback:
                callbacks.append(callback)
        return callbacks
