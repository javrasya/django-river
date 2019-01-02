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
        from river.models.fields.state import workflow_registry

        for field_name in workflow_registry.workflows:
            transition_approval_meta = self.get_model('TransitionApprovalMeta').objects.filter(field_name=field_name)
            if transition_approval_meta.count() == 0:
                LOGGER.warning("%s field doesn't seem have any transition approval meta in database" % field_name)

        if isinstance(handler_backend, DatabaseHandlerBackend):
            try:
                self.get_model('Handler').objects.exists()
                handler_backend.initialize_handlers()
            except (OperationalError, ProgrammingError):
                LOGGER.debug('Database handlers are not registered. Because database is not created yet.')
        LOGGER.debug('RiverApp is loaded.')
