from django.contrib.contenttypes.models import ContentType

from river.models import State, TransitionApprovalMeta
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException


class ClassWorkflowObject(object):

    def __init__(self, workflow_class, name, field_name):
        self.workflow_class = workflow_class
        self.name = name
        self.field_name = field_name

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.workflow_class)

    def get_on_approval_objects(self, as_user):
        object_pks = []
        for workflow_object in self.workflow_class.objects.all():
            instance_workflow = getattr(workflow_object.river, self.name)
            transition_approvals = instance_workflow.get_available_approvals(as_user=as_user)
            if transition_approvals.count():
                object_pks.append(workflow_object.pk)
        return self.workflow_class.objects.filter(pk__in=object_pks)

    @property
    def initial_state(self):
        initial_states = State.objects.filter(
            pk__in=TransitionApprovalMeta.objects.filter(
                content_type=self._content_type,
                field_name=self.name,
                parents__isnull=True
            ).values_list("source_state", flat=True)
        )
        if initial_states.count() == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_INITIAL_STATE, 'There is no available initial state for the content type %s. ' % self._content_type)
        elif initial_states.count() > 1:
            raise RiverException(ErrorCode.MULTIPLE_INITIAL_STATE,
                                 'There are multiple initial state for the content type %s. Have only one initial state' % self._content_type)

        return initial_states[0]

    @property
    def final_states(self):
        return State.objects.filter(
            pk__in=TransitionApprovalMeta.objects.filter(
                field_name=self.name,
                children__isnull=True,
                content_type=self._content_type
            ).values_list("destination_state", flat=True)
        )