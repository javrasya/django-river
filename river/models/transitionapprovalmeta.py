from __future__ import unicode_literals

from django.db import models, transaction
from django.db.models import PROTECT
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext_lazy as _

from river.config import app_config
from river.models import Workflow
from river.models.base_model import BaseModel
from river.models.managers.transitionmetada import TransitionApprovalMetadataManager
from river.models.transitionmeta import TransitionMeta


class TransitionApprovalMeta(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Transition Approval Meta")
        verbose_name_plural = _("Transition Approval Meta")
        unique_together = [('workflow', 'transition_meta', 'priority')]

    objects = TransitionApprovalMetadataManager()

    workflow = models.ForeignKey(Workflow, verbose_name=_("Workflow"), related_name='transition_approval_metas', on_delete=PROTECT)

    transition_meta = models.ForeignKey(TransitionMeta, verbose_name=_("Transition Meta"), related_name='transition_approval_meta', on_delete=PROTECT)

    permissions = models.ManyToManyField(app_config.PERMISSION_CLASS, verbose_name=_('Permissions'), blank=True)
    groups = models.ManyToManyField(app_config.GROUP_CLASS, verbose_name=_('Groups'), blank=True)
    priority = models.IntegerField(default=0, verbose_name=_('Priority'), null=True)
    parents = models.ManyToManyField('self', verbose_name='parents', related_name='children', symmetrical=False, db_index=True, blank=True)

    def __str__(self):
        return 'Transition: %s,Permissions: %s, Groups: %s, Order: %s' % (
            self.transition_meta,
            ','.join(self.permissions.values_list('name', flat=True)),
            ','.join(self.groups.values_list('name', flat=True)), self.priority)


def post_save_model(sender, instance, *args, **kwargs):
    parents = TransitionApprovalMeta.objects \
        .filter(workflow=instance.workflow, transition_meta__destination_state=instance.transition_meta.source_state) \
        .exclude(pk__in=instance.parents.values_list('pk', flat=True)) \
        .exclude(pk=instance.pk)

    children = TransitionApprovalMeta.objects \
        .filter(workflow=instance.workflow, transition_meta__source_state=instance.transition_meta.destination_state) \
        .exclude(parents__in=[instance.pk]) \
        .exclude(pk=instance.pk)

    instance = TransitionApprovalMeta.objects.get(pk=instance.pk)
    if parents:
        instance.parents.add(*parents)

    for child in children:
        child.parents.add(instance)


@transaction.atomic
def pre_delete_model(sender, instance, *args, **kwargs):
    from river.models.transitionapproval import PENDING
    instance.transition_approvals.filter(status=PENDING).delete()


post_save.connect(post_save_model, sender=TransitionApprovalMeta)
pre_delete.connect(pre_delete_model, sender=TransitionApprovalMeta)
