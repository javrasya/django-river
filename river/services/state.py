from django.db.models import Q

from river.models.transition import FORWARD
from river.models.proceeding import Proceeding
from river.models.state import State
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException
from .proceeding import ProceedingService

__author__ = 'ahmetdal'


class StateService:
    def __init__(self):
        pass

    @staticmethod
    def get_state_by(**kwargs):
        if kwargs:
            return State.objects.get(**kwargs)

    @staticmethod
    def get_current_state(workflow_object, field):
        return getattr(workflow_object, field)

    @staticmethod
    def get_available_states(workflow_object, field, user, include_user=True):
        current_state = getattr(workflow_object, field)
        proceedings = Proceeding.objects.filter(
            field=field,
            workflow_object=workflow_object,
            meta__transition__source_state=current_state,
        )
        if include_user:
            proceedings = proceedings.filter(
                meta__permissions__in=user.user_permissions.all()
            )
        destination_states = proceedings.values_list('meta__transition__destination_state', flat=True)
        return State.objects.filter(pk__in=destination_states)

    @staticmethod
    def get_initial_state(content_type, field):
        """
        A state which is not a destination of a transition but can be source of a transition OR not (a destination of a transition and this transition direction is FORWARD)
        """
        states = State.objects.filter(pk__in=ProceedingService.get_initial_proceedings(content_type, field).values_list('meta__transition__source_state', flat=True))
        if states.count() == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_INITIAL_STATE, 'There is no available initial state for the content type %s. ' % content_type)
        elif states.count() > 1:
            raise RiverException(ErrorCode.MULTIPLE_INITIAL_STATE, 'There are multiple initial state for the content type %s. Have only one initial state' % content_type)

        return states[0]

    @staticmethod
    def get_final_states(content_type, field):

        """
        A state which is not a source of a transition but can be destination of a transition OR not (a source of a transition and this transition direction is FORWARD)
        """
        proceedings = ProceedingService.get_final_proceedings(content_type, field)
        if proceedings.count() == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_FINAL_STATE, 'There is no available final state for the content type %s.' % content_type)

        return State.objects.filter(pk__in=proceedings.values_list('meta__transition__destination_state', flat=True))
