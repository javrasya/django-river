from django.db import models

__author__ = 'ahmetdal'


class WorkflowManager(models.Manager):
    def get_by_natural_key(self, content_type, field_name):
        return self.get(content_type=content_type, field_name=field_name)
