import logging
from river.handlers.backends.base import powerset

from river.handlers.backends.memory import MemoryHandlerBackend
from river.models.handler import Handler

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class DatabaseHandlerBackend(MemoryHandlerBackend):

    def initialize_handlers(self):
        self.__register(Handler.objects.filter(enabled=True))

    def __register(self, handler_objs):
        handlers = []
        if handler_objs.exists():
            for handler in handler_objs:
                if handler.hash not in self.handlers:
                    module, method_name = handler.method.rsplit('.', 1)
                    try:
                        method = getattr(__import__(module, fromlist=[method_name]), method_name, None)
                        if method:
                            self.handlers[handler.hash] = method
                            handlers.append(method)
                            LOGGER.debug("Handler '%s' from database is registered initially from database as method '%s' and module '%s'. " % (handler.hash, method_name, module))
                        else:
                            LOGGER.warning("Handler '%s' from database can not be registered. Because method '%s' is not in module '%s'. " % (handler.hash, method_name, module))
                    except ImportError:
                        LOGGER.warning("Handler '%s' from database can not be registered. Because module '%s'  does not exists. " % (handler.hash, module))
        return handlers

    def register(self, handler_cls, handler, workflow_object, field, override=False, *args, **kwargs):
        hash = super(DatabaseHandlerBackend, self).register(handler_cls, handler, workflow_object, field, override=override, *args, **kwargs)
        handler_obj, created = Handler.objects.update_or_create(
            hash=hash,
            defaults={
                'method': '%s.%s' % (handler.__module__, handler.__name__),
                'handler_cls': '%s.%s' % (handler_cls.__module__, handler_cls.__name__),
            }
        )
        if created:
            LOGGER.debug("Handler '%s' is registered in database as method %s and module %s. " % (handler_obj.hash, handler.__name__, handler.__module__))
        else:
            LOGGER.warning("Handler '%s' is already registered in database as method %s and module %s. " % (handler_obj.hash, handler.__name__, handler.__module__))

        return hash

    def get_handlers(self, handler_cls, workflow_object, field, *args, **kwargs):
        handlers = super(DatabaseHandlerBackend, self).get_handlers(handler_cls, workflow_object, field, *args, **kwargs)
        if not handlers:
            hashes = []
            for c in powerset(kwargs.keys()):
                skwargs = {}
                for f in c:
                    skwargs[f] = kwargs.get(f)
                hash = self.get_handler_class(handler_cls).get_hash(workflow_object, field, **skwargs)
                hashes.append(self.get_handler_class_prefix(self.get_handler_class(handler_cls)) + hash)
            handlers = self.__register(Handler.objects.filter(hash__in=hashes))
        return handlers
