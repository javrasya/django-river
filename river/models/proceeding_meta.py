from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from river.config import app_config
from river.models.base_model import BaseModel
from river.models.managers.proceeding_meta import ProceedingMetaManager
from river.models.transition import Transition

__author__ = 'ahmetdal'


@python_2_unicode_compatible
class ProceedingMeta(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Proceeding Meta")
        verbose_name_plural = _("Proceeding Metas")
        unique_together = [('content_type', 'transition', 'order')]

    objects = ProceedingMetaManager()

    content_type = models.ForeignKey(app_config.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'))

    transition = models.ForeignKey(Transition, verbose_name=_('Transition'))
    permissions = models.ManyToManyField(app_config.PERMISSION_CLASS, verbose_name=_('Permissions'), blank=True)
    groups = models.ManyToManyField(app_config.GROUP_CLASS, verbose_name=_('Groups'), blank=True)
    order = models.IntegerField(default=0, verbose_name=_('Order'), null=True)
    action_text = models.TextField(_("Action Text"), max_length=200, null=True, blank=True)

    parents = models.ManyToManyField('self', verbose_name='parents', related_name='children', symmetrical=False,
                                     db_index=True, blank=True)

    def natural_key(self):
        return self.content_type, self.transition, self.order

    def __str__(self):
        return 'Transition:%s, Permissions:%s, Groups:%s, Order:%s' % (
            self.transition, ','.join(self.permissions.values_list('name', flat=True)),
            ','.join(self.groups.values_list('name', flat=True)), self.order)


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


def post_save_model(sender, instance, *args, **kwargs):
    from river.services.proceeding_meta import ProceedingMetaService
    ProceedingMetaService.build_tree(instance)


m2m_changed.connect(post_group_change, sender=ProceedingMeta.groups.through)
m2m_changed.connect(post_permissions_change, sender=ProceedingMeta.permissions.through)

post_save.connect(post_save_model, sender=ProceedingMeta)
