from django.contrib.contenttypes.models import ContentType

from django.db import models

from river.services.object import ObjectService

__author__ = 'ahmetdal'


class WorkflowObjectManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(WorkflowObjectManager, self).__init__()

    def get_objects_waiting_for_approval(self, user):
        return ObjectService.get_objects_waiting_for_approval(ContentType.objects.get_for_model(self.model), user)

    def get_object_count_waiting_for_approval(self, user):
        return ObjectService.get_object_count_waiting_for_approval(ContentType.objects.get_for_model(self.model), user)
