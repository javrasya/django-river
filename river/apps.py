import logging

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class RiverApp(AppConfig):
    name = 'river'
    label = 'river'

    def ready(self):

        from river.handlers.backends.database import DatabaseHandlerBackend
        from river.handlers.backends.loader import handler_backend        

        if isinstance(handler_backend, DatabaseHandlerBackend):
            try:
                self.get_model('Handler').objects.exists()
                handler_backend.initialize_handlers()
            except (OperationalError, ProgrammingError):
                LOGGER.debug('Database handlers are not registered. Because database is not created yet.')
        LOGGER.debug('RiverApp is loaded.')
