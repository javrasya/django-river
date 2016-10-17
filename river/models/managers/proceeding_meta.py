from django.db import models

__author__ = 'ahmetdal'


class ProceedingMetaManager(models.Manager):
    def get_by_natural_key(self, content_type, transition, order):
        return self.get(content_type=content_type, transition=transition, order=order)
