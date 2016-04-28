import logging
from datetime import datetime

from django.db.transaction import atomic

from river.models.proceeding import APPROVED
from river.services.proceeding import ProceedingService
from river.services.state import StateService
from river.signals import ProceedingSignal, TransitionSignal, FinalSignal
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
    def proceed(workflow_object, field, user, next_state=None, god_mod=False):

        def process(workflow_object, field, user, action, next_state=None, god_mod=False):
            current_state = getattr(workflow_object, field)
            proceedings = ProceedingService.get_available_proceedings(workflow_object, field, [current_state],
                                                                      user=user, god_mod=god_mod)
            c = proceedings.count()
            if c == 0:
                raise RiverException(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER,
                                     "There is no available state for destination for the user.")
            if c > 1:
                if next_state:
                    proceedings = proceedings.filter(meta__transition__destination_state=next_state)
                    if proceedings.count() == 0:
                        available_states = StateService.get_available_states(workflow_object, field, user)
                        raise RiverException(ErrorCode.INVALID_NEXT_STATE_FOR_USER,
                                             "Invalid state is given(%s). Valid states is(are) %s" % (
                                                 next_state.__unicode__(),
                                                 ','.join([ast.__unicode__() for ast in available_states])))
                else:
                    raise RiverException(ErrorCode.NEXT_STATE_IS_REQUIRED,
                                         "State must be given when there are multiple states for destination")
            proceeding = proceedings[0]
            proceeding.status = action
            proceeding.transactioner = user
            proceeding.transaction_date = datetime.now()
            if workflow_object.proceeding:
                proceeding.previous = workflow_object.proceeding
            proceeding.save()


            return proceeding

        proceeding = process(workflow_object, field, user, APPROVED, next_state, god_mod)

        current_state = getattr(workflow_object, field)

        # Any other proceeding is left?
        required_proceedings = ProceedingService.get_available_proceedings(workflow_object, field, [current_state],
                                                                           destination_state=next_state,
                                                                           god_mod=god_mod)

        transition_status = False
        if required_proceedings.count() == 0:
            setattr(workflow_object, field, proceeding.meta.transition.destination_state)
            transition_status = True

            # Next states should be PENDING back again if there is circle.
            ProceedingService.cycle_proceedings(workflow_object, field)
            # ProceedingService.get_next_proceedings(workflow_object, field).update(status=PENDING)

        with ProceedingSignal(workflow_object, field, proceeding), TransitionSignal(transition_status,
                                                                                    workflow_object, field,
                                                                                    proceeding), FinalSignal(
            workflow_object, field):
            workflow_object.save()

        LOGGER.debug("Workflow object %s for field %s is proceeded for next transition. Transition: %s -> %s" % (
            workflow_object, field, current_state.label, getattr(workflow_object, field).label))
