from django.db import models
from river.models.fields.state import StateField

__author__ = 'ahmetdal'


class TestModel(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)
    my_field = StateField()

    objects = models.Manager()
