from river.models.proceeding import Proceeding
from river.services.proceeding import ProceedingService
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


# noinspection PyClassHasNoInit
class ObjectService:
    @staticmethod
    def register_object(workflow_object):
        proceedings = Proceeding.objects.filter(workflow_object=workflow_object)
        if proceedings.count() == 0:
            ProceedingService.init_proceedings(workflow_object)

    @staticmethod
    def get_objects_waiting_for_approval(content_type, user):
        object_pks = []
        WorkflowObjectClass = content_type.model_class()
        for workflow_object in WorkflowObjectClass.objects.all():
            proceedings = ProceedingService.get_available_proceedings(workflow_object, [workflow_object.get_state()], user=user)
            if proceedings.count():
                object_pks.append(workflow_object.pk)
        return WorkflowObjectClass.objects.filter(pk__in=object_pks)

    @staticmethod
    def get_object_count_waiting_for_approval(content_type, user):
        return ObjectService.get_objects_waiting_for_approval(content_type, user).count()

    @staticmethod
    def is_workflow_completed(workflow_object):
        return Proceeding.objects.filter(workflow_object=workflow_object, meta__transition__source_state=workflow_object.get_state()).count() == 0

    @staticmethod
    def get_field(workflow_class):
        from river.models.fields.state import StateField

        field = next((f for f in workflow_class._meta.fields if type(f) is StateField), None)

        if not field:
            raise RiverException(ErrorCode.NO_STATE_FIELD, "There is no state field in model class of given instance")

        return field
