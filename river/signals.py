import logging

from django.dispatch import Signal

__author__ = 'ahmetdal'

pre_final = Signal(providing_args=["workflow_object", ])
post_final = Signal(providing_args=["workflow_object", ])

pre_transition = Signal(providing_args=["workflow_object", "source_state", "destination_state", "proceeding"])
post_transition = Signal(providing_args=["workflow_object", "source_state", "destination_state", "proceeding"])

pre_proceed = Signal(providing_args=["workflow_object", "proceeding"])
post_proceed = Signal(providing_args=["workflow_object", "proceeding"])

LOGGER = logging.getLogger(__name__)


class TransitionSignal(object):
    def __init__(self, status, workflow_object, proceeding):
        self.status = status
        self.workflow_object = workflow_object
        self.proceeding = proceeding

    def __enter__(self):
        if self.status:
            pre_transition.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                source_state=self.proceeding.meta.transition.source_state,
                destination_state=self.proceeding.meta.transition.destination_state,
                proceeding=self.proceeding,
            )
            LOGGER.debug("Pre transition signal IS sent for workflow object %s for transition %s -> %s" % (
                self.workflow_object, self.proceeding.meta.transition.source_state.label, self.proceeding.meta.transition.destination_state.label))
        else:
            LOGGER.debug(
                "Pre transition signal IS NOT sent for workflow object %s. Although proceeding is occurred, not transition is occurred." % (
                    self.workflow_object))

    def __exit__(self, type, value, traceback):
        if self.status:
            post_transition.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                source_state=self.proceeding.meta.transition.source_state,
                destination_state=self.proceeding.meta.transition.destination_state,
                proceeding=self.proceeding,
            )
            LOGGER.debug(
                "Post transition signal IS sent for workflow object %s for transition %s -> %s" % (
                    self.workflow_object, self.proceeding.meta.transition.source_state.label, self.proceeding.meta.transition.destination_state.label))
        else:
            LOGGER.debug(
                "Post transition signal IS NOT sent for workflow object %s. Although proceeding is occurred, not transition is occurred." % (
                    self.workflow_object))


class ProceedingSignal(object):
    def __init__(self, workflow_object, proceeding):
        self.workflow_object = workflow_object
        self.proceeding = proceeding

    def __enter__(self):
        pre_proceed.send(
            sender=ProceedingSignal.__class__,
            workflow_object=self.workflow_object,
            proceeding=self.proceeding,
        )
        LOGGER.debug("Pre proceeding signal IS sent for workflow object %s for transition %s -> %s" % (
            self.workflow_object, self.proceeding.meta.transition.source_state.label, self.proceeding.meta.transition.destination_state.label))

    def __exit__(self, type, value, traceback):
        post_proceed.send(
            sender=TransitionSignal.__class__,
            workflow_object=self.workflow_object,
            proceeding=self.proceeding,
        )
        LOGGER.debug("Post proceeding signal IS sent for workflow object %s for transition %s -> %s" % (
            self.workflow_object, self.proceeding.meta.transition.source_state.label, self.proceeding.meta.transition.destination_state.label))


class FinalSignal(object):
    def __init__(self, workflow_object):
        self.workflow_object = workflow_object
        self.status = self.workflow_object.on_final_state

    def __enter__(self):
        if self.status:
            pre_final.send(
                sender=FinalSignal.__class__,
                workflow_object=self.workflow_object,
            )
            LOGGER.debug("Pre final signal IS sent for workflow object %s for final state %s" % (self.workflow_object, self.workflow_object.get_state().label))

    def __exit__(self, type, value, traceback):
        if self.status:
            post_final.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
            )
            LOGGER.debug("Post final signal IS sent for workflow object %s for final state %s" % (self.workflow_object, self.workflow_object.get_state().label))
