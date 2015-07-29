from river.models.approvement import Approvement

__author__ = 'ahmetdal'


# noinspection PyClassHasNoInit
class ApprovementMetaService:
    @staticmethod
    def apply_new_approvement_meta(new_approvement_meta):
        if new_approvement_meta.approvements.count() == 0:
            content_type = new_approvement_meta.transition.content_type
            WorkflowObjectClass = content_type.model_class()
            field = new_approvement_meta.transition.field
            Approvement.objects.bulk_create(
                list(
                    Approvement(
                        workflow_object=workflow_object,
                        meta=new_approvement_meta,
                        field=field,
                        content_type=content_type
                    )
                    for workflow_object in WorkflowObjectClass.objects.all()
                )
            )
