from django.db import models

from django.db.models.signals import m2m_changed

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
    permissions = models.ManyToManyField(RiverConfig.PERMISSION_CLASS, verbose_name=_('Permissions'))
    groups = models.ManyToManyField(RiverConfig.GROUP_CLASS, verbose_name=_('Groups'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    action_text = models.TextField(_("Approve Text"), max_length=200, null=True, blank=True)

    def __unicode__(self):
        return 'Transition:%s, Permissions:%s, Order:%s' % (self.transition, ','.join(self.permissions.values_list('name', flat=True)), self.order)


def post_group_change(sender, instance, *args, **kwargs):
    from river.services.approvement import ApprovementService
    from river.models.approvement import PENDING

    for approvement_pending in instance.approvements.filter(status=PENDING):
        ApprovementService.override_groups(approvement_pending, instance.groups.all())


def post_permissions_change(sender, instance, *args, **kwargs):
    from river.models.approvement import PENDING
    from river.services.approvement import ApprovementService

    for approvement_pending in instance.approvements.filter(status=PENDING):
        ApprovementService.override_permissions(approvement_pending, instance.permissions.all())


m2m_changed.connect(post_group_change, sender=ApprovementMeta.groups.through)
m2m_changed.connect(post_permissions_change, sender=ApprovementMeta.permissions.through)
