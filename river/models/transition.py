from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.state import State
from river.services.config import RiverConfig

__author__ = 'ahmetdal'

BACKWARD = 0
FORWARD = 1

DIRECTIONS = [
    (BACKWARD, _("Backward")),
    (FORWARD, _("Forward"))
]


class Transition(BaseModel):
    class Meta:
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")

    content_type = models.ForeignKey(RiverConfig.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'))
    field = models.CharField(verbose_name=_('Field'), max_length=200)
    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transitions_as_source')
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"), related_name='transitions_as_destination')
    direction = models.SmallIntegerField(_("Transition Direction"), default=FORWARD)

    def __unicode__(self):
        return '%s -> %s (%s)' % (self.source_state, self.destination_state, self.content_type)
