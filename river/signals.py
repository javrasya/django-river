import logging

from django.dispatch import Signal

__author__ = 'ahmetdal'

pre_on_complete = Signal(providing_args=["workflow_object", "field_name", ])
post_on_complete = Signal(providing_args=["workflow_object", "field_name", ])

pre_transition = Signal(providing_args=["workflow_object", "field_name", "source_state", "destination_state"])
post_transition = Signal(providing_args=["workflow_object", "field_name", "source_state", "destination_state"])

pre_approve = Signal(providing_args=["workflow_object", "field_name", "transition_approval"])
post_approve = Signal(providing_args=["workflow_object", "field_name", "transition_approval"])

LOGGER = logging.getLogger(__name__)


class TransitionSignal(object):
    def __init__(self, status, workflow_object, field_name, transition_approval):
        self.status = status
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.transition_approval = transition_approval

    def __enter__(self):
        if self.status:
            pre_transition.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                field_name=self.field_name,
                source_state=self.transition_approval.source_state,
                destination_state=self.transition_approval.destination_state
            )
            LOGGER.debug("The signal that is fired right before the transition ( %s -> %s ) happened for %s" % (
                self.transition_approval.source_state.label, self.transition_approval.destination_state.label, self.workflow_object))

    def __exit__(self, type, value, traceback):
        if self.status:
            post_transition.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                field_name=self.field_name,
                source_state=self.transition_approval.source_state,
                destination_state=self.transition_approval.destination_state,
                transition_approval=self.transition_approval,
            )
            LOGGER.debug("The signal that is fired right after the transition ( %s -> %s ) happened for %s" % (
                self.transition_approval.source_state.label, self.transition_approval.destination_state.label, self.workflow_object))


class ApproveSignal(object):
    def __init__(self, workflow_object, field_name, transition_approval):
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.transition_approval = transition_approval

    def __enter__(self):
        pre_approve.send(
            sender=ApproveSignal.__class__,
            workflow_object=self.workflow_object,
            field_name=self.field_name,
            transition_approval=self.transition_approval,
        )
        LOGGER.debug("The signal that is fired right before a transition approval is approved for %s due to transition %s -> %s" % (
            self.workflow_object, self.transition_approval.source_state.label, self.transition_approval.destination_state.label))

    def __exit__(self, type, value, traceback):
        post_approve.send(
            sender=ApproveSignal.__class__,
            workflow_object=self.workflow_object,
            field_name=self.field_name,
            source_state=self.transition_approval.source_state,
            destination_state=self.transition_approval.destination_state
        )
        LOGGER.debug("The signal that is fired right after a transition approval is approved for %s due to transition %s -> %s" % (
            self.workflow_object, self.transition_approval.source_state.label, self.transition_approval.destination_state.label))


class OnCompleteSignal(object):
    def __init__(self, workflow_object, field_name):
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.workflow = getattr(self.workflow_object.river, self.field_name)
        self.status = self.workflow.on_final_state

    def __enter__(self):
        if self.status:
            pre_on_complete.send(
                sender=OnCompleteSignal.__class__,
                workflow_object=self.workflow_object,
                field_name=self.field_name,
            )
            LOGGER.debug("The signal that is fired right before the workflow of %s is complete" % self.workflow_object)

    def __exit__(self, type, value, traceback):
        if self.status:
            post_on_complete.send(
                sender=OnCompleteSignal.__class__,
                workflow_object=self.workflow_object,
                field_name=self.field_name,
            )
            LOGGER.debug("The signal that is fired right after the workflow of %s is complete" % self.workflow_object)
