from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.managers.workflow import WorkflowManager

__author__ = 'ahmetdal'


@python_2_unicode_compatible
class Workflow(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Workflow")
        verbose_name_plural = _("Workflows")

    objects = WorkflowManager()

    name = models.SlugField(unique=True, null=True, blank=True)
    description = models.CharField(_("Description"), max_length=200, null=True, blank=True)

    def __str__(self):
        return self.label

    def natural_key(self):
        return self.name,


def on_pre_save(sender, instance, *args, **kwargs):
    instance.name = slugify(instance.name)


pre_save.connect(on_pre_save, Workflow)
