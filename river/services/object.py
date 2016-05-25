from river.models.proceeding import Proceeding
from river.services.proceeding import ProceedingService
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


# noinspection PyClassHasNoInit
class ObjectService:
    @staticmethod
    def register_object(workflow_object, field):
        proceedings = Proceeding.objects.filter(workflow_object=workflow_object, field=field)
        if proceedings.count() == 0:
            ProceedingService.init_proceedings(workflow_object, field)

    @staticmethod
    def get_objects_waiting_for_approval(content_type, field, user):
        object_pks = []
        WorkflowObjectClass = content_type.model_class()
        for workflow_object in WorkflowObjectClass.objects.all():
            current_state = getattr(workflow_object, field)
            proceedings = ProceedingService.get_available_proceedings(workflow_object, field, [current_state],
                                                                      user=user)
            if proceedings.count():
                object_pks.append(workflow_object.pk)
        return WorkflowObjectClass.objects.filter(pk__in=object_pks)

    @staticmethod
    def get_object_count_waiting_for_approval(content_type, field, user):
        return ObjectService.get_objects_waiting_for_approval(content_type, field, user).count()

    @staticmethod
    def is_workflow_completed(workflow_object, field):
        current_state = getattr(workflow_object, field)
        return Proceeding.objects.filter(workflow_object=workflow_object,
                                         meta__transition__source_state=current_state).count() == 0

    @staticmethod
    def get_the_fields(workflow_class):
        from river.models.fields.state import StateField
        return [f for f in workflow_class._meta.fields if type(f) is StateField]

    @staticmethod
    def get_only_field(workflow_class):
        fields = ObjectService.get_the_fields(workflow_class)

        if not len(fields):
            raise RiverException(ErrorCode.NO_STATE_FIELD,
                                 "There is no state field in model class of given instance")

        elif len(fields) > 1:
            raise RiverException(ErrorCode.MULTIPLE_STATE_FIELDS,
                                 "There are multiple state field in the instance model class. Please send which field will be used")

        return fields[0]
