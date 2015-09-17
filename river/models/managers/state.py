from django.db import models

__author__ = 'ahmetdal'


class StateManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
