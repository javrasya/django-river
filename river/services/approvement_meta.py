from river.models import Object
from river.models.approvement import Approvement

__author__ = 'ahmetdal'


# noinspection PyClassHasNoInit
class ApprovementMetaService:
    @staticmethod
    def apply_new_approvement_meta(new_approvement_meta):
        if new_approvement_meta.approvement_set.count() == 0:
            content_type = new_approvement_meta.transition.content_type
            field = new_approvement_meta.transition.field
            Approvement.objects.bulk_create(
                list(
                    Approvement(
                        object_id=obj_id,
                        meta=new_approvement_meta,
                        field=field,
                        content_type=content_type
                    )
                    for obj_id in Object.objects.values_list('object_id', flat=True)
                )
            )
