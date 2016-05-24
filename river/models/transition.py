from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.managers.transition import TransitionManager
from river.models.state import State

__author__ = 'ahmetdal'

BACKWARD = 0
FORWARD = 1

DIRECTIONS = [
    (BACKWARD, _("Backward")),
    (FORWARD, _("Forward"))
]


class Transition(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")
        unique_together = (('source_state', 'destination_state'),)

    objects = TransitionManager()

    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transitions_as_source')
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"),
                                          related_name='transitions_as_destination')
    direction = models.SmallIntegerField(_("Transition Direction"), choices=DIRECTIONS, default=FORWARD)

    def natural_key(self):
        return self.source_state.slug, self.destination_state.slug

    def __unicode__(self):
        return '%s -> %s' % (self.source_state, self.destination_state)
