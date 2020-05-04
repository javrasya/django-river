from django.contrib.contenttypes.models import ContentType

from river.driver.mssql_driver import MsSqlDriver
from river.driver.orm_driver import OrmDriver
from river.models import State, TransitionApprovalMeta, Workflow, app_config


class ClassWorkflowObject(object):

    def __init__(self, workflow_object_class, field_name, workflow=None):
        self.workflow_object_class = workflow_object_class
        self.field_name = field_name
        # TODO : Fix
        print("class workflow")
        self.workflow = workflow or Workflow.objects.get(id=self.workflow_object_class.objects.first().workflow_id)
        self._cached_river_driver = None

    @property
    def _river_driver(self):
        if self._cached_river_driver:
            return self._cached_river_driver
        else:
            if app_config.IS_MSSQL:
                self._cached_river_driver = MsSqlDriver(self.workflow, self.workflow_object_class, self.field_name)
            else:
                self._cached_river_driver = OrmDriver(self.workflow, self.workflow_object_class, self.field_name)
            return self._cached_river_driver

    def get_on_approval_objects(self, as_user):
        approvals = self.get_available_approvals(as_user)
        object_ids = list(approvals.values_list('object_id', flat=True))
        return self.workflow_object_class.objects.filter(pk__in=object_ids)

    def get_available_approvals(self, as_user):
        return self._river_driver.get_available_approvals(as_user)

    @property
    def initial_state(self):
        workflow = Workflow.objects.filter(content_type=self._content_type, field_name=self.field_name).first()
        return workflow.initial_state if workflow else None

    @property
    def final_states(self):
        final_approvals = TransitionApprovalMeta.objects.filter(workflow=self.workflow, children__isnull=True)
        return State.objects.filter(pk__in=final_approvals.values_list("transition_meta__destination_state", flat=True))

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.workflow_object_class)
