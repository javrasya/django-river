from django.contrib.contenttypes.models import ContentType

from river.models import State, TransitionApprovalMeta, Workflow


class ClassWorkflowObject(object):

    def __init__(self, workflow_class, name, field_name):
        self.workflow_class = workflow_class
        self.name = name
        self.field_name = field_name
        self._cached_workflow = None

    @property
    def workflow(self):
        if not self._cached_workflow:
            self._cached_workflow = Workflow.objects.filter(field_name=self.field_name, content_type=self._content_type).first()
        return self._cached_workflow

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.workflow_class)

    def get_available_approvals(self, as_user):
        transition_approvals = None
        for workflow_object in self.workflow_class.objects.all():
            instance_workflow = getattr(workflow_object.river, self.name)
            available_approvals = instance_workflow.get_available_approvals(as_user=as_user)
            transition_approvals = available_approvals.union(available_approvals) if transition_approvals else available_approvals

        return transition_approvals

    def get_on_approval_objects(self, as_user):
        available_approvals = self.get_available_approvals(as_user)
        return self.workflow_class.objects.filter(pk__in=available_approvals.values_list("object_id", flat=True))

    @property
    def initial_state(self):
        workflow = Workflow.objects.filter(content_type=self._content_type, field_name=self.name).first()
        return workflow.initial_state if workflow else None

    @property
    def final_states(self):
        return State.objects.filter(
            pk__in=TransitionApprovalMeta.objects.filter(
                workflow=self.workflow,
                children__isnull=True
            ).values_list("destination_state", flat=True)
        )
