from river.models.approvement import Approvement
from river.models.object import Object
from river.services.approvement import ApprovementService
from river.services.state import StateService

__author__ = 'ahmetdal'


# noinspection PyClassHasNoInit
class ObjectService:
    @staticmethod
    def register_object(content_type_id, object_id, field_id):
        approvements = Approvement.objects.filter(content_type__pk=content_type_id, object_id=object_id, field__pk=field_id)
        if approvements.count() == 0:
            ApprovementService.init_approvements(content_type_id, object_id, field_id)

        initial_state = StateService.get_init_state(content_type_id, field_id)
        obj = Object.objects.get(object_id=object_id)
        obj.state = initial_state
        obj.save()

        return {'state': initial_state.details()}


    @staticmethod
    def get_objects_waiting_for_approval(content_type_id, field_id, user_id):
        object_pks = []
        objects = Object.objects.filter(content_type__pk=content_type_id, field__pk=field_id)
        for obj in objects:
            current_state = obj.state
            approvements = ApprovementService.get_approvements_object_waiting_for_approval(content_type_id, obj.object_id, field_id, user_id, [current_state])
            if approvements.count():
                object_pks.append(obj.pk)
        return Object.objects.filter(pk__in=object_pks)


    @staticmethod
    def get_object_count_waiting_for_approval(content_type_id, field_id, user_id):
        return ObjectService.get_objects_waiting_for_approval(content_type_id, field_id, user_id).count()
