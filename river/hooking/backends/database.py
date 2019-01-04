import logging

from river.hooking.backends.base import powerset
from river.hooking.backends.memory import MemoryHookingBackend
from river.models.callback import Callback

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class DatabaseHookingBackend(MemoryHookingBackend):

    def initialize_callbacks(self):
        self.__register(Callback.objects.filter(enabled=True))

    def __register(self, callback_objs):
        callbacks = []
        if callback_objs.exists():
            for callback in callback_objs:
                if callback.hash not in self.callbacks:
                    module, method_name = callback.method.rsplit('.', 1)
                    try:
                        method = getattr(__import__(module, fromlist=[method_name]), method_name, None)
                        if method:
                            self.callbacks[callback.hash] = method
                            callbacks.append(method)
                            LOGGER.debug("Callback '%s' from database is registered initially from database as method '%s' and module '%s'. " % (callback.hash, method_name, module))
                        else:
                            LOGGER.warning("Callback '%s' from database can not be registered. Because method '%s' is not in module '%s'. " % (callback.hash, method_name, module))
                    except ImportError:
                        LOGGER.warning("Callback '%s' from database can not be registered. Because module '%s'  does not exists. " % (callback.hash, module))
        return callbacks

    def register(self, hooking_cls, callback, workflow_object, field_name, override=False, *args, **kwargs):
        hash = super(DatabaseHookingBackend, self).register(hooking_cls, callback, workflow_object, field_name, override=override, *args, **kwargs)
        callback_obj, created = Callback.objects.update_or_create(
            hash=hash,
            defaults={
                'method': '%s.%s' % (callback.__module__, callback.__name__),
                'hooking_cls': '%s.%s' % (hooking_cls.__module__, hooking_cls.__name__),
            }
        )
        if created:
            LOGGER.debug("Callback '%s' is registered in database as method %s and module %s. " % (callback_obj.hash, callback.__name__, callback.__module__))
        else:
            LOGGER.debug("Callback '%s' is already registered in database as method %s and module %s. " % (callback_obj.hash, callback.__name__, callback.__module__))

        return hash

    def get_callbacks(self, hooking_cls, workflow_object, field_name, *args, **kwargs):
        callbacks = super(DatabaseHookingBackend, self).get_callbacks(hooking_cls, workflow_object, field_name, *args, **kwargs)
        if not callbacks:
            hashes = []
            for c in powerset(kwargs.keys()):
                skwargs = {}
                for f in c:
                    skwargs[f] = kwargs.get(f)
                hash = self.get_hooking_class(hooking_cls).get_hash(workflow_object, field_name, **skwargs)
                hashes.append(self.get_hooking_class_prefix(self.get_hooking_class(hooking_cls)) + hash)
            callbacks = self.__register(Callback.objects.filter(hash__in=hashes))
        return callbacks
