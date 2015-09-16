from django.db import models

from django.db.models.signals import m2m_changed

from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.transition import Transition
from river.services.config import RiverConfig

__author__ = 'ahmetdal'


class ProceedingMetaManager(models.Manager):
    def get_by_natural_key(self, content_type, field, transition, order):
        return self.get(content_type=content_type, field=field, transition=transition, order=order)


class ProceedingMeta(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Proceeding Meta")
        verbose_name_plural = _("Proceeding Metas")
        unique_together = [('content_type', 'field', 'transition', 'order')]

    objects = ProceedingMetaManager()

    content_type = models.ForeignKey(RiverConfig.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'))
    field = models.CharField(verbose_name=_('Field'), max_length=200)

    transition = models.ForeignKey(Transition, verbose_name=_('Transition'))
    permissions = models.ManyToManyField(RiverConfig.PERMISSION_CLASS, verbose_name=_('Permissions'))
    groups = models.ManyToManyField(RiverConfig.GROUP_CLASS, verbose_name=_('Groups'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    action_text = models.TextField(_("Action Text"), max_length=200, null=True, blank=True)

    def natural_key(self):
        return self.content_type, self.field, self.transition, self.order

    def __unicode__(self):
        return 'Transition:%s, Permissions:%s, Order:%s' % (self.transition, ','.join(self.permissions.values_list('name', flat=True)), self.order)


def post_group_change(sender, instance, *args, **kwargs):
    from river.services.proceeding import ProceedingService
    from river.models.proceeding import PENDING

    for proceeding_pending in instance.proceedings.filter(status=PENDING):
        ProceedingService.override_groups(proceeding_pending, instance.groups.all())


def post_permissions_change(sender, instance, *args, **kwargs):
    from river.models.proceeding import PENDING
    from river.services.proceeding import ProceedingService

    for proceeding_pending in instance.proceedings.filter(status=PENDING):
        ProceedingService.override_permissions(proceeding_pending, instance.permissions.all())


m2m_changed.connect(post_group_change, sender=ProceedingMeta.groups.through)
m2m_changed.connect(post_permissions_change, sender=ProceedingMeta.permissions.through)
