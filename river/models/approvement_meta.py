from django.db import models

from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.transition import Transition
from river.services.config import RiverConfig

__author__ = 'ahmetdal'


class ApprovementMeta(BaseModel):
    class Meta:
        verbose_name = _("Approvement Meta")
        verbose_name_plural = _("Approvement Metas")
        unique_together = [('transition', 'order')]

    transition = models.ForeignKey(Transition, verbose_name=_('Transition'))
    permissions = models.ManyToManyField(RiverConfig.PERMISSION_CLASS, verbose_name=_('Permissions'), null=True)
    groups = models.ManyToManyField(RiverConfig.GROUP_CLASS, verbose_name=_('Groups'), null=True)
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    def __unicode__(self):
        return 'Transition:%s, Permissions:%s, Order:%s' % (self.transition, ','.join(self.permissions.values_list('name', flat=True)), self.order)
