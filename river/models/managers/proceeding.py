from django.db import models

from river.config import app_config

__author__ = 'ahmetdal'


class ProceedingManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(ProceedingManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwarg):
        object = kwarg.pop('workflow_object', None)
        if object:
            kwarg['content_type'] = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(object)
            kwarg['object_id'] = object.pk

        return super(ProceedingManager, self).filter(*args, **kwarg)

    def update_or_create(self, *args, **kwarg):
        object = kwarg.pop('workflow_object', None)
        if object:
            kwarg['content_type'] = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(object)
            kwarg['object_id'] = object.pk

        return super(ProceedingManager, self).update_or_create(*args, **kwarg)
