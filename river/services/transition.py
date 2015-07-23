from datetime import datetime
from river.models.approvement import APPROVED, REJECTED
from river.models.field import Field
from river.models.object import Object
from river.models.state import State
from river.services.approvement import ApprovementService
from river.services.state import StateService
from river.utils.exceptions import RiverIOException

__author__ = 'ahmetdal'


class TransitionService:
    def __init__(self):
        pass

    @staticmethod
    def approve_transition(content_type_id, object_id, field_id, user_id, next_state_id=None):
        content_type = ExternalContentType.objects.get(pk=content_type_id)
        field = Field.objects.get(pk=field_id)
        obj = Object.objects.get(content_type=content_type, object_id=object_id, field=field)
        approvement = TransitionService.process(content_type_id, object_id, field_id, user_id, APPROVED, next_state_id)
        current_state = obj.state
        required_approvements = ApprovementService.get_approvements_object_waiting_for_approval(content_type_id, object_id, field_id, user_id, [current_state], include_user=False,
                                                                                                destination_state_id=next_state_id)
        if required_approvements.count() == 0:
            obj.state = approvement.meta.transition.destination_state
            obj.save()

    @staticmethod
    def reject_transition(content_type_id, object_id, field_id, user_id, next_state_id=None):
        TransitionService.process(content_type_id, object_id, field_id, user_id, REJECTED, next_state_id)

    @staticmethod
    def process(content_type_id, object_id, field_id, user_id, action, next_state_id=None):
        obj = Object.objects.get(content_type_id=content_type_id, object_id=object_id, field_id=field_id)
        current_state = obj.state
        next_state = None
        if next_state_id:
            next_state = State.objects.get(pk=next_state_id)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(content_type_id, object_id, field_id, user_id, [current_state])
        c = approvements.count()
        if c == 0:
            raise RiverIOException("There is no available state for destination for the user.")
        if c > 1:
            if next_state:
                approvements = approvements.filter(meta__transition__destination_state=next_state)
                if approvements.count() == 0:
                    available_states = StateService.get_available_states(content_type_id, object_id, field_id, user_id)
                    raise RiverIOException("Invalid state is given(%s). Valid states is(are) %s" % (next_state.__unicode__(), ','.join([ast.__unicode__() for ast in available_states])))
            else:
                raise RiverIOException("State must be given when there are multiple states for destination")
        approvement = approvements[0]
        approvement.status = action
        approvement.transactioner = ExternalUser.objects.get(user_id=user_id)
        approvement.transaction_date = datetime.now()
        approvement.save()
        return approvement
