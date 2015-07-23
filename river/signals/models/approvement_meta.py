from django.db.models.signals import post_save

from apps.riverio.models.approvement_meta import ApprovementMeta
from apps.riverio.services.approvement_meta import ApprovementMetaService


__author__ = 'ahmetdal'


def on_post_save(sender, instance, *args, **kwargs):
    if kwargs.get("created", False):
        ApprovementMetaService.apply_new_approvement_meta(instance)


post_save.connect(on_post_save, ApprovementMeta)