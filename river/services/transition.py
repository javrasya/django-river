from datetime import datetime
from django.db.transaction import atomic

from river.models.approvement import APPROVED, REJECTED, Approvement, PENDING
from river.services.approvement import ApprovementService
from river.services.state import StateService
from river.signals import workflow_is_completed, on_transition
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


class TransitionService(object):
    def __init__(self):
        pass

    @staticmethod
    @atomic
    def approve_transition(workflow_object, field, user, next_state=None, god_mod=False):
        approvement = TransitionService.process(workflow_object, field, user, APPROVED, next_state, god_mod)

        current_state = getattr(workflow_object, field)
        # Any other approvement is left?
        required_approvements = ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, [current_state], destination_state=next_state, god_mod=god_mod)
        if required_approvements.count() == 0:
            setattr(workflow_object, field, approvement.meta.transition.destination_state)
            workflow_object.save()

            # Next states should be PENDING back again if there is circle.
            Approvement.objects.filter(workflow_object=workflow_object, field=field, meta__transition__source_state=approvement.meta.transition.destination_state).update(status=PENDING)

        if current_state != getattr(workflow_object, field):
            on_transition.send(sender=TransitionService.__class__, workflow_object=workflow_object, field=field, source_state=current_state, destination_state=getattr(workflow_object, field))
        if workflow_object.on_final_state:
            workflow_is_completed.send(sender=TransitionService, workflow_object=workflow_object, field=field)

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

        return approvement
