import logging

from django.dispatch import Signal

__author__ = 'ahmetdal'

pre_final = Signal(providing_args=["workflow_object", "field_name", ])
post_final = Signal(providing_args=["workflow_object", "field_name", ])

pre_transition = Signal(providing_args=["workflow_object", "field_name", "transition_approval"])
post_transition = Signal(providing_args=["workflow_object", "field_name", "transition_approval"])

pre_proceed = Signal(providing_args=["workflow_object", "field_name", "proceeding"])
post_proceed = Signal(providing_args=["workflow_object", "field_name", "proceeding"])

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
                destination_state=self.transition_approval.destination_state,
                transition_approval=self.transition_approval,
            )
            LOGGER.debug("Pre transition signal IS sent for workflow object %s for transition %s -> %s" % (
                self.workflow_object, self.transition_approval.source_state.label, self.transition_approval.destination_state.label))
        else:
            LOGGER.debug(
                "Pre transition signal IS NOT sent for workflow object %s. Although transition_approval is occurred, not transition is occurred." % (
                    self.workflow_object))

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
            LOGGER.debug(
                "Post transition signal IS sent for workflow object %s for transition %s -> %s" % (
                    self.workflow_object, self.transition_approval.source_state.label, self.transition_approval.destination_state.label))
        else:
            LOGGER.debug(
                "Post transition signal IS NOT sent for workflow object %s. Although transition_approval is occurred, not transition is occurred." % (
                    self.workflow_object))


class ProceedingSignal(object):
    def __init__(self, workflow_object, field_name, transition_approval):
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.transition_approval = transition_approval

    def __enter__(self):
        pre_proceed.send(
            sender=ProceedingSignal.__class__,
            workflow_object=self.workflow_object,
            field_name=self.field_name,
            transition_approval=self.transition_approval,
        )
        LOGGER.debug("Pre transition approval signal is sent for workflow object %s for transition %s -> %s" % (
            self.workflow_object, self.transition_approval.source_state.label, self.transition_approval.destination_state.label))

    def __exit__(self, type, value, traceback):
        post_proceed.send(
            sender=TransitionSignal.__class__,
            workflow_object=self.workflow_object,
            field_name=self.field_name,
            transition_approval=self.transition_approval,
        )
        LOGGER.debug("Post transition approval signal is sent for workflow object %s for transition %s -> %s" % (
            self.workflow_object, self.transition_approval.source_state.label, self.transition_approval.destination_state.label))


class FinalSignal(object):
    def __init__(self, workflow_object, field_name):
        self.workflow_object = workflow_object
        self.field_name = field_name
        self.workflow = getattr(self.workflow_object.river, self.field_name)
        self.status = self.workflow.on_final_state

    def __enter__(self):
        if self.status:
            pre_final.send(
                sender=FinalSignal.__class__,
                workflow_object=self.workflow_object,
                field_name=self.field_name,
            )
            LOGGER.debug("Pre final signal is sent for workflow object %s for final state %s" % (self.workflow_object, self.workflow.get_state().label))

    def __exit__(self, type, value, traceback):
        if self.status:
            post_final.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                field_name=self.field_name,
            )
            LOGGER.debug("Post final signal is sent for workflow object %s for final state %s" % (self.workflow_object, self.workflow.get_state().label))
