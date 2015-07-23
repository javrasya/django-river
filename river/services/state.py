from river.models.approvement import Approvement
from river.models.state import State
from river.utils.exceptions import RiverException

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
        approvements = Approvement.objects.filter(
            field=field,
            object=workflow_object,
            meta__transition__source_state=current_state,
        )
        if include_user:
            approvements = approvements.filter(
                meta__permissions__in=user.user_permissions.all()
            )
        destination_states = approvements.values_list('meta__transition__destination_state', flat=True)
        return State.objects.filter(pk__in=destination_states)

    @staticmethod
    def get_init_state(content_type, field):
        initial_state_candidates = State.objects.filter(
            transitions_as_source__isnull=False,
            transitions_as_source__content_type=content_type,
            transitions_as_source__field=field,
            transitions_as_destination__isnull=True,
        ).distinct()
        c = initial_state_candidates.count()
        if c == 0:
            raise RiverException('There is no available initial state for the content type %s. Insert a state which is not a destination in a transition.' % content_type)
        elif c > 1:
            raise RiverException('There are multiple initial state for the content type %s. Have only one initial state' % content_type)

        return initial_state_candidates[0]
