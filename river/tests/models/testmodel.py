from django.db import models

from river.models.fields.state import StateField

__author__ = 'ahmetdal'


class TestModel(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)
    my_field = StateField(workflow_name="test_workflow1")


class TestModelWithoutStateField(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)


class TestModelSlowCase1(models.Model):
    status = StateField(workflow_name="test_workflow2")


class TestModelSlowCase2(models.Model):
    status = StateField(workflow_name="test_workflow3")
