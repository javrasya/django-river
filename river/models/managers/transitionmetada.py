from django.db import models

__author__ = 'ahmetdal'


class TransitionApprovalMetadataManager(models.Manager):
    def get_by_natural_key(self, workflow, source_state, destination_state, priority):
        return self.get(workflow=workflow, source_state=source_state, destination_state=destination_state, priority=priority)
