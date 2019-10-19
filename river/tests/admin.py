from django.contrib import admin
from django.contrib.admin import ModelAdmin

from river.tests.models import BasicTestModel


class BasicTestModelAdmin(ModelAdmin):
    pass


admin.site.register(BasicTestModel, BasicTestModelAdmin)
