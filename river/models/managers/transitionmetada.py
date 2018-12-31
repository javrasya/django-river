from django.db import models

__author__ = 'ahmetdal'


class TransitionApprovalMetadataManager(models.Manager):
    def get_by_natural_key(self, content_type, transition, priority):
        return self.get(content_type=content_type, transition=transition, priority=priority)
