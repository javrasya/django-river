from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeOneToOneField

from river.models import Approvement
from river.models.base_model import BaseModel

__author__ = 'ahmetdal'


class ApprovementTrack(BaseModel):
    class Meta:
        verbose_name = _("Approvement Track")
        verbose_name_plural = _("Approvement Tracks")

    approvement = models.ForeignKey(Approvement, verbose_name=_('Approvement'), related_name="tracks")

    process_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    previous_track = TreeOneToOneField("self", verbose_name=_('Previous track'), related_name="next_track", null=True, blank=True)
