from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.riverio.models.base_model import BaseModel
from apps.riverio.models.external_contenttype import ExternalContentType
from apps.riverio.models.field import Field
from apps.riverio.models.state import State


__author__ = 'ahmetdal'


class Transition(BaseModel):
    class Meta:
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")

    content_type = models.ForeignKey(ExternalContentType, verbose_name=_('Content Type'))
    field = models.ForeignKey(Field, verbose_name=_('Content Type'))
    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transitions_as_source')
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"), related_name='transitions_as_destination')


    def __unicode__(self):
        return '%s -> %s (%s)' % (self.source_state, self.destination_state, self.content_type)



