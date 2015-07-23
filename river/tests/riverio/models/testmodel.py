from django.db import models


__author__ = 'ahmetdal'


class TestModel(models.Model):
    test_field = models.CharField(max_length=50, null=True, blank=True)
