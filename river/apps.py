import logging

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from river.config import app_config
from river.handlers.backends.database import DatabaseHandlerBackend
from river.handlers.backends.loader import handler_backend

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class RiverApp(AppConfig):
    name = 'river'
    label = 'river'

    def ready(self):
        if isinstance(handler_backend, DatabaseHandlerBackend):
            try:
                self.get_model('Handler').objects.exists()
                handler_backend.initialize_handlers()
            except (OperationalError, ProgrammingError):
                LOGGER.debug('Database handlers are not registered. Because database is not created yet.')

        LOGGER.debug('RiverApp is loaded.')
