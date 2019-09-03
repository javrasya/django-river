from django.db import models

from river.models.fields.state import StateField

__author__ = 'ahmetdal'


class BasicTestModel(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)
    my_field = StateField()


class ModelWithoutStateField(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)


class ModelForSlowCase1(models.Model):
    status = StateField()


class ModelForSlowCase2(models.Model):
    status = StateField()
