from django.db import models
from django.utils.translation import ugettext_lazy as _
from river.models.base_model import BaseModel

__author__ = 'ahmetdal'


class Field(BaseModel):
    class Meta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")
        ordering = ('created_at',)

    label = models.CharField(max_length=50)
    description = models.CharField(_("Description"), max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.label
