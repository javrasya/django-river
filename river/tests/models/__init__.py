from uuid import uuid4

from django.db import models

from river.models import Workflow
from river.models.fields.state import StateField


class BasicTestModel(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)
    test_field = models.CharField(max_length=50, null=True, blank=True)
    my_field = StateField()


class BasicTestModelWithoutAdmin(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)
    my_field = StateField()


class ModelWithoutStateField(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)


class ModelForSlowCase1(models.Model):
    status = StateField()


class ModelForSlowCase2(models.Model):
    status = StateField()


class ModelWithTwoStateFields(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)
    status1 = StateField()
    status2 = StateField()


class ModelWithStringPrimaryKey(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)
    custom_pk = models.CharField(max_length=200, primary_key=True, default=uuid4())
    status = StateField()
