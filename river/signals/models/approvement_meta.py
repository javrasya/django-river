from django.db.models.signals import post_save

from river.models.approvement_meta import ApprovementMeta
from river.services.approvement_meta import ApprovementMetaService

__author__ = 'ahmetdal'


def on_post_save(sender, instance, *args, **kwargs):
    if kwargs.get("created", False):
        ApprovementMetaService.apply_new_approvement_meta(instance)
        if set(instance.approvements.values_list('permissions__pk')) != set(instance.permissions.values_list('pk')):
            for approvement in instance.approvements.all():
                approvement.permissions.clear()
                approvement.permissions.add(*instance.permissions)

        if set(instance.approvements.values_list('groups__pk')) != set(instance.groups.values_list('pk')):
            for approvement in instance.approvements.all():
                approvement.groups.clear()
                approvement.groups.add(*instance.groups)


post_save.connect(on_post_save, ApprovementMeta)
