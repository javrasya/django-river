import logging

from django.apps import AppConfig
from river.handlers.backends.database import DatabaseHandlerBackend
from river.handlers.backends.loader import handler_backend

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class RiverApp(AppConfig):
    name = 'river'
    label = 'river'

    def ready(self):
        if isinstance(handler_backend, DatabaseHandlerBackend):
            handler_backend.initialize_handlers()
        LOGGER.debug('RiverApp is loaded.')
