from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel

from river.models.field import Field
from river.models.state import State
from river.services.config import RiverConfig

__author__ = 'ahmetdal'


class Object(BaseModel):
    class Meta:
        verbose_name = _("Object")
        verbose_name_plural = _("Objects")
        ordering = ('created_at',)
        unique_together = [('object_id', 'content_type', 'field')]

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(RiverConfig.CONTENT_TYPE_CLASS, verbose_name=_("Content Type"))
    object = generic.GenericForeignKey('content_type', 'object_pk')

    field = models.ForeignKey(Field, verbose_name=_("Field"))
    state = models.ForeignKey(State, verbose_name=_("Description"))
    description = models.CharField(_('Description'), max_length=200, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.state, self.description)

    def details(self):
        detail = super(Object, self).details()
        detail.update(
            {
                'object_id': self.object_id,
                'state_id': self.state.pk
            }
        )
        return detail
