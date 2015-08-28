from datetime import datetime

from django.db.transaction import atomic
import logging

from river.models.approvement import APPROVED, REJECTED, PENDING
from river.services.approvement import ApprovementService
from river.services.state import StateService
from river.signals import pre_final, post_final, pre_transition, post_transition, pre_approved, post_approved, ApprovementSignal, TransitionSignal, FinalSignal
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


class TTSSignal(object):
    def __init__(self, status, pre_signal, post_signal, **kwargs):
        self.status = status
        self.pre_signal = pre_signal
        self.post_signal = post_signal
        self.kwargs = kwargs

    def __enter__(self):
        if self.status:
            self.pre_signal.send(
                sender=TTSSignal.__class__,
                **self.kwargs
            )

    def __exit__(self, type, value, traceback):
        if self.status:
            self.post_signal.send(
                sender=TTSSignal.__class__,
                **self.kwargs
            )


LOGGER = logging.getLogger(__name__)


class TransitionService(object):
    def __init__(self):
        pass

    @staticmethod
    @atomic
    def approve_transition(workflow_object, field, user, next_state=None, god_mod=False):

        approvement, track = TransitionService.process(workflow_object, field, user, APPROVED, next_state, god_mod)
        workflow_object.approvement_track = track

        current_state = getattr(workflow_object, field)
        # Any other approvement is left?
        required_approvements = ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, [current_state], destination_state=next_state, god_mod=god_mod)

        transition_status = False
        if required_approvements.count() == 0:
            setattr(workflow_object, field, approvement.meta.transition.destination_state)
            transition_status = True

            # Next states should be PENDING back again if there is circle.
            ApprovementService.get_next_approvements(workflow_object, field).update(status=PENDING)

        with ApprovementSignal(workflow_object, field, approvement, track), TransitionSignal(transition_status, workflow_object, field, approvement), FinalSignal(workflow_object, field):
            workflow_object.save()

        LOGGER.debug("Workflow object %s for field %s is approved for next transition. Transition: %s -> %s" % (workflow_object, field, current_state.label, getattr(workflow_object, field).label))

    @staticmethod
    @atomic
    def reject_transition(workflow_object, field, user, next_state=None):
        TransitionService.process(workflow_object, field, user, REJECTED, next_state)

    @staticmethod
    def process(workflow_object, field, user, action, next_state=None, god_mod=False):
        current_state = getattr(workflow_object, field)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, [current_state], user=user, god_mod=god_mod)
        c = approvements.count()
        if c == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, "There is no available state for destination for the user.")
        if c > 1:
            if next_state:
                approvements = approvements.filter(meta__transition__destination_state=next_state)
                if approvements.count() == 0:
                    available_states = StateService.get_available_states(workflow_object, field, user)
                    raise RiverException(ErrorCode.INVALID_NEXT_STATE_FOR_USER,
                                         "Invalid state is given(%s). Valid states is(are) %s" % (next_state.__unicode__(), ','.join([ast.__unicode__() for ast in available_states])))
            else:
                raise RiverException(ErrorCode.NEXT_STATE_IS_REQUIRED, "State must be given when there are multiple states for destination")
        approvement = approvements[0]
        approvement.status = action
        approvement.transactioner = user
        approvement.transaction_date = datetime.now()
        approvement.save()

        c = False
        track = workflow_object.approvement_track
        while not c:
            track, c = approvement.tracks.get_or_create(previous_track=track)
        return approvement, track
