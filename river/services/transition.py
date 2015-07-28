from datetime import datetime

from river.models.approvement import APPROVED, REJECTED
from river.services.approvement import ApprovementService
from river.services.object import ObjectService
from river.services.state import StateService
from river.signals import workflow_is_completed, on_transition
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


class TransitionService(object):
    def __init__(self):
        pass

    @staticmethod
    def approve_transition(workflow_object, field, user, next_state=None):
        approvement = TransitionService.process(workflow_object, field, user, APPROVED, next_state)
        current_state = getattr(workflow_object, field)
        # Any other approvement is left?
        required_approvements = ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, user, [current_state], include_user=False, destination_state=next_state)
        if required_approvements.count() == 0:
            setattr(workflow_object, field, approvement.meta.transition.destination_state)
            workflow_object.save()

        if current_state != getattr(workflow_object, field):
            on_transition.send(sender=TransitionService.__class__, workflow_object=workflow_object, field=field, source_state=current_state, destination_state=getattr(workflow_object, field))
        if ObjectService.is_workflow_completed(workflow_object, field):
            workflow_is_completed.send(sender=TransitionService, workflow_object=workflow_object, field=field)

    @staticmethod
    def reject_transition(workflow_object, field, user, next_state=None):
        TransitionService.process(workflow_object, field, user, REJECTED, next_state)

    @staticmethod
    def process(workflow_object, field, user, action, next_state=None):
        current_state = getattr(workflow_object, field)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, user, [current_state])
        c = approvements.count()
        if c == 0:
            raise RiverException("There is no available state for destination for the user.")
        if c > 1:
            if next_state:
                approvements = approvements.filter(meta__transition__destination_state=next_state)
                if approvements.count() == 0:
                    available_states = StateService.get_available_states(workflow_object, field, user)
                    raise RiverException("Invalid state is given(%s). Valid states is(are) %s" % (next_state.__unicode__(), ','.join([ast.__unicode__() for ast in available_states])))
            else:
                raise RiverException("State must be given when there are multiple states for destination")
        approvement = approvements[0]
        approvement.status = action
        approvement.transactioner = user
        approvement.transaction_date = datetime.now()
        approvement.save()
        return approvement
