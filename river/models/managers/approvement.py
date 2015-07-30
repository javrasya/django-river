from django.contrib.contenttypes.models import ContentType
from django.db import models
from river.services.config import RiverConfig

__author__ = 'ahmetdal'


class ApprovementManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(ApprovementManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwarg):
        object = kwarg.pop('workflow_object', None)
        if object:
            kwarg['content_type'] = RiverConfig.CONTENT_TYPE_CLASS.objects.get_for_model(object)
            kwarg['object_id'] = object.pk

        return super(ApprovementManager, self).filter(*args, **kwarg)

    def update_or_create(self, *args, **kwarg):
        object = kwarg.pop('workflow_object', None)
        if object:
            kwarg['content_type'] = RiverConfig.CONTENT_TYPE_CLASS.objects.get_for_model(object)
            kwarg['object_id'] = object.pk

        return super(ApprovementManager, self).update_or_create(*args, **kwarg)
