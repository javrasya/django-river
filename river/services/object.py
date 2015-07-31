from river.models.approvement import Approvement
from river.services.approvement import ApprovementService

__author__ = 'ahmetdal'


# noinspection PyClassHasNoInit
class ObjectService:
    @staticmethod
    def register_object(workflow_object, field):
        approvements = Approvement.objects.filter(workflow_object=workflow_object, field=field)
        if approvements.count() == 0:
            ApprovementService.init_approvements(workflow_object, field)

        return {'state': getattr(workflow_object, field).details()}

    @staticmethod
    def get_objects_waiting_for_approval(content_type, field, user):
        object_pks = []
        WorkflowObjectClass = content_type.model_class()
        for workflow_object in WorkflowObjectClass.objects.all():
            current_state = getattr(workflow_object, field)
            approvements = ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, [current_state], user=user)
            if approvements.count():
                object_pks.append(workflow_object.pk)
        return WorkflowObjectClass.objects.filter(pk__in=object_pks)

    @staticmethod
    def get_object_count_waiting_for_approval(content_type, field, user):
        return ObjectService.get_objects_waiting_for_approval(content_type, field, user).count()

    @staticmethod
    def is_workflow_completed(workflow_object, field):
        current_state = getattr(workflow_object, field)
        return Approvement.objects.filter(workflow_object=workflow_object, meta__transition__source_state=current_state).count() == 0
