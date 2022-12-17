import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.dispatch import Signal

from river.models import Workflow
from river.models.hook import BEFORE, AFTER
from river.models.on_approved_hook import OnApprovedHook
from river.models.on_complete_hook import OnCompleteHook
from river.models.on_transit_hook import OnTransitHook

pre_on_complete = Signal()
post_on_complete = Signal()

pre_transition = Signal()
post_transition = Signal()

pre_approve = Signal()
post_approve = Signal()

LOGGER = logging.getLogger(__name__)


class TransitionSignal(object):
    def __init__(self, status, workflow_object, field_name, transition_approval):
        self.status = status
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.transition_approval = transition_approval
        self.content_type = ContentType.objects.get_for_model(self.workflow_object.__class__)
        self.workflow = Workflow.objects.get(content_type=self.content_type, field_name=self.field_name)

    def __enter__(self):
        if self.status:
            for hook in OnTransitHook.objects.filter(
                    (Q(object_id__isnull=True) | Q(object_id=self.workflow_object.pk, content_type=self.content_type)) &
                    (Q(transition__isnull=True) | Q(transition=self.transition_approval.transition)) &
                    Q(
                        workflow__field_name=self.field_name,
                        transition_meta=self.transition_approval.transition.meta,
                        hook_type=BEFORE
                    )
            ):
                hook.execute(self._get_context(BEFORE))

            LOGGER.debug("The signal that is fired right before the transition ( %s ) happened for %s"
                         % (self.transition_approval.transition, self.workflow_object))

    def __exit__(self, type, value, traceback):
        if self.status:
            for hook in OnTransitHook.objects.filter(
                    (Q(object_id__isnull=True) | Q(object_id=self.workflow_object.pk, content_type=self.content_type)) &
                    (Q(transition__isnull=True) | Q(transition=self.transition_approval.transition)) &
                    Q(
                        workflow=self.workflow,
                        transition_meta=self.transition_approval.transition.meta,
                        hook_type=AFTER
                    )
            ):
                hook.execute(self._get_context(AFTER))
            LOGGER.debug("The signal that is fired right after the transition ( %s) happened for %s"
                         % (self.transition_approval.transition, self.workflow_object))

    def _get_context(self, when):
        return {
            "hook": {
                "type": "on-transit",
                "when": when,
                "payload": {
                    "workflow": self.workflow,
                    "workflow_object": self.workflow_object,
                    "transition_approval": self.transition_approval
                }
            },
        }


class ApproveSignal(object):
    def __init__(self, workflow_object, field_name, transition_approval):
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.transition_approval = transition_approval
        self.content_type = ContentType.objects.get_for_model(self.workflow_object.__class__)
        self.workflow = Workflow.objects.get(content_type=self.content_type, field_name=self.field_name)

    def __enter__(self):
        for hook in OnApprovedHook.objects.filter(
                (Q(object_id__isnull=True) | Q(object_id=self.workflow_object.pk, content_type=self.content_type)) &
                (Q(transition_approval__isnull=True) | Q(transition_approval=self.transition_approval)) &
                Q(
                    workflow__field_name=self.field_name,
                    transition_approval_meta=self.transition_approval.meta,
                    hook_type=BEFORE
                )
        ):
            hook.execute(self._get_context(BEFORE))

        LOGGER.debug("The signal that is fired right before a transition approval is approved for %s due to transition %s -> %s" % (
            self.workflow_object, self.transition_approval.transition.source_state.label, self.transition_approval.transition.destination_state.label))

    def __exit__(self, type, value, traceback):
        for hook in OnApprovedHook.objects.filter(
                (Q(object_id__isnull=True) | Q(object_id=self.workflow_object.pk, content_type=self.content_type)) &
                (Q(transition_approval__isnull=True) | Q(transition_approval=self.transition_approval)) &
                Q(
                    workflow__field_name=self.field_name,
                    transition_approval_meta=self.transition_approval.meta,
                    hook_type=AFTER
                )
        ):
            hook.execute(self._get_context(AFTER))
        LOGGER.debug("The signal that is fired right after a transition approval is approved for %s due to transition %s -> %s" % (
            self.workflow_object, self.transition_approval.transition.source_state.label, self.transition_approval.transition.destination_state.label))

    def _get_context(self, when):
        return {
            "hook": {
                "type": "on-approved",
                "when": when,
                "payload": {
                    "workflow": self.workflow,
                    "workflow_object": self.workflow_object,
                    "transition_approval": self.transition_approval
                }
            },
        }


class OnCompleteSignal(object):
    def __init__(self, workflow_object, field_name):
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.workflow = getattr(self.workflow_object.river, self.field_name)
        self.status = self.workflow.on_final_state
        self.content_type = ContentType.objects.get_for_model(self.workflow_object.__class__)
        self.workflow = Workflow.objects.get(content_type=self.content_type, field_name=self.field_name)

    def __enter__(self):
        if self.status:
            for hook in OnCompleteHook.objects.filter(
                    (Q(object_id__isnull=True) | Q(object_id=self.workflow_object.pk, content_type=self.content_type)) &
                    Q(
                        workflow__field_name=self.field_name,
                        hook_type=BEFORE
                    )
            ):
                hook.execute(self._get_context(BEFORE))
            LOGGER.debug("The signal that is fired right before the workflow of %s is complete" % self.workflow_object)

    def __exit__(self, type, value, traceback):
        if self.status:
            for hook in OnCompleteHook.objects.filter(
                    (Q(object_id__isnull=True) | Q(object_id=self.workflow_object.pk, content_type=self.content_type)) &
                    Q(
                        workflow__field_name=self.field_name,
                        hook_type=AFTER
                    )
            ):
                hook.execute(self._get_context(AFTER))
            LOGGER.debug("The signal that is fired right after the workflow of %s is complete" % self.workflow_object)

    def _get_context(self, when):
        return {
            "hook": {
                "type": "on-complete",
                "when": when,
                "payload": {
                    "workflow": self.workflow,
                    "workflow_object": self.workflow_object,
                }
            },
        }
