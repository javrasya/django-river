from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeOneToOneField

from river.models import Proceeding
from river.models.base_model import BaseModel

__author__ = 'ahmetdal'


class ProceedingTrack(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Proceeding Track")
        verbose_name_plural = _("Proceeding Tracks")

    proceeding = models.ForeignKey(Proceeding, verbose_name=_('Proceeding'), related_name="tracks")

    process_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    previous_track = TreeOneToOneField("self", verbose_name=_('Previous track'), related_name="next_track", null=True, blank=True)


