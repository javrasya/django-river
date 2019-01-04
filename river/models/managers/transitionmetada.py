from django.db import models

__author__ = 'ahmetdal'


class TransitionApprovalMetadataManager(models.Manager):
    def get_by_natural_key(self, field_name, content_type, source_state, destination_state, priority):
        return self.get(field_name=field_name, content_type=content_type, source_state=source_state, destination_state=destination_state, priority=priority)
