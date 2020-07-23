from django.contrib.contenttypes.models import ContentType

from river.driver.mssql_driver import MsSqlDriver
from river.driver.orm_driver import OrmDriver
from river.models import State, TransitionApprovalMeta, Workflow, app_config, TransitionMeta


class ClassWorkflowObject(object):

    def __init__(self, wokflow_object_class, field_name):
        self.wokflow_object_class = wokflow_object_class
        self.field_name = field_name
        self.workflow = Workflow.objects.filter(field_name=self.field_name, content_type=self._content_type).first()
        self._cached_river_driver = None

    @property
    def _river_driver(self):
        if self._cached_river_driver:
            return self._cached_river_driver
        else:
            if app_config.IS_MSSQL:
                self._cached_river_driver = MsSqlDriver(self.workflow, self.wokflow_object_class, self.field_name)
            else:
                self._cached_river_driver = OrmDriver(self.workflow, self.wokflow_object_class, self.field_name)
            return self._cached_river_driver

    def get_on_approval_objects(self, as_user):
        approvals = self.get_available_approvals(as_user)
        object_ids = list(approvals.values_list('object_id', flat=True))
        return self.wokflow_object_class.objects.filter(pk__in=object_ids)

    def get_available_approvals(self, as_user):
        return self._river_driver.get_available_approvals(as_user)

    @property
    def initial_state(self):
        workflow = Workflow.objects.filter(content_type=self._content_type, field_name=self.field_name).first()
        return workflow.initial_state if workflow else None

    @property
    def final_states(self):
        all_states = TransitionMeta.objects.filter(workflow=self.workflow).values_list("source_state", "destination_state")
        source_states = set([states[0] for states in all_states])
        destination_states = set([states[1] for states in all_states])
        final_states = destination_states - source_states
        return State.objects.filter(pk__in=final_states)

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.wokflow_object_class)
