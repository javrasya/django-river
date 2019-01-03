from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel

__author__ = 'ahmetdal'


class Callback(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Callback")
        verbose_name_plural = _("Callbacks")

    hash = models.CharField(_('Hash'), max_length=200, unique=True)
    method = models.CharField(_('Callback Method'), max_length=200)
    hooking_cls = models.CharField(_('HookingClass'), max_length=200)
    enabled = models.BooleanField(_('Enabled'), default=True)
