from river.models.approvement import Approvement
from river.models.field import Field
from river.models.object import Object
from river.models.state import State
from river.utils.exceptions import RiverIOException

__author__ = 'ahmetdal'


class StateService:
    def __init__(self):
        pass

    @staticmethod
    def get_state_by(**kwargs):
        if kwargs:
            return State.objects.get(**kwargs)

    @staticmethod
    def get_current_state(content_type_id, object_id, field_id):
        content_type = ExternalContentType.objects.get(pk=content_type_id)
        field = Field.objects.get(pk=field_id)
        obj = Object.objects.get(content_type=content_type, field=field, object_id=object_id)
        return obj.state

    @staticmethod
    def get_available_states(content_type_id, object_id, field_id, user_id, include_user=True):
        content_type = ExternalContentType.objects.get(pk=content_type_id)
        field = Field.objects.get(pk=field_id)
        obj = Object.objects.get(content_type=content_type, field=field, object_id=object_id)
        current_state = obj.state
        approvements = Approvement.objects.filter(
            content_type=content_type,
            field=field,
            object_id=object_id,
            meta__transition__source_state=current_state,
        )
        if include_user:
            user = ExternalUser.objects.get(user_id=user_id)
            approvements = approvements.filter(
                meta__permission__in=user.permissions.all()
            )
        destination_states = approvements.values_list('meta__transition__destination_state', flat=True)
        return State.objects.filter(pk__in=destination_states)

    @staticmethod
    def get_init_state(content_type_id, field_id):
        content_type = ExternalContentType.objects.get(pk=content_type_id)
        field = Field.objects.get(pk=field_id)
        initial_state_candidates = State.objects.filter(
            transitions_as_source__isnull=False,
            transitions_as_source__content_type=content_type,
            transitions_as_source__field=field,
            transitions_as_destination__isnull=True,
        ).distinct()
        c = initial_state_candidates.count()
        if c == 0:
            raise RiverIOException('There is no available initial state for the content type %s. Insert a state which is not a destination in a transition.' % content_type)
        elif c > 1:
            raise RiverIOException('There are multiple initial state for the content type %s. Have only one initial state' % content_type)

        return initial_state_candidates[0]
