from django.db import models
from river.models.state import State

__author__ = 'ahmetdal'


class TransitionManager(models.Manager):
    def get_by_natural_key(self, source_state, destination_state):
        return self.get(source_state=State.objects.get_by_natural_key(source_state), destination_state=State.objects.get_by_natural_key(destination_state))
