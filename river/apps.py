import logging
import operator
from functools import reduce

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class RiverApp(AppConfig):
    name = 'river'
    label = 'river'

    def ready(self):

        from river.hooking.backends.database import DatabaseHookingBackend
        from river.hooking.backends.loader import callback_backend

        for field_name in self._get_all_workflow_fields():
            try:
                workflows = self.get_model('Workflow').objects.filter(field_name=field_name)
                if workflows.count() == 0:
                    LOGGER.warning("%s field doesn't seem have any workflow defined in database. You should create its workflow" % field_name)
            except (OperationalError, ProgrammingError):
                pass

        if isinstance(callback_backend, DatabaseHookingBackend):
            try:
                self.get_model('Callback').objects.exists()
                callback_backend.initialize_callbacks()
            except (OperationalError, ProgrammingError):
                pass
        LOGGER.debug('RiverApp is loaded.')

    @classmethod
    def _get_all_workflow_fields(cls):
        from river.core.workflowregistry import workflow_registry
        return reduce(operator.concat, map(list, workflow_registry.workflows.values()), [])
