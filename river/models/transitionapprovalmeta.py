from __future__ import unicode_literals

from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from river.config import app_config
from river.models import State, Workflow
from river.models.base_model import BaseModel
from river.models.managers.transitionmetada import TransitionApprovalMetadataManager

__author__ = 'ahmetdal'


class TransitionApprovalMeta(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Transition Approval Meta")
        verbose_name_plural = _("Transition Approval Meta")
        unique_together = [('workflow', 'source_state', 'destination_state', 'priority')]

    objects = TransitionApprovalMetadataManager()

    workflow = models.ForeignKey(Workflow, verbose_name=_("Workflow"), related_name='transition_approval_metas', on_delete=CASCADE)

    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transition_approval_meta_as_source', on_delete=CASCADE)
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"), related_name='transition_approval_meta_as_destination', on_delete=CASCADE)

    permissions = models.ManyToManyField(app_config.PERMISSION_CLASS, verbose_name=_('Permissions'), blank=True)
    groups = models.ManyToManyField(app_config.GROUP_CLASS, verbose_name=_('Groups'), blank=True)
    priority = models.IntegerField(default=0, verbose_name=_('Priority'), null=True)
    parents = models.ManyToManyField('self', verbose_name='parents', related_name='children', symmetrical=False, db_index=True, blank=True)

    def natural_key(self):
        return self.workflow, self.source_state, self.destination_state, self.priority

    def __str__(self):
        return 'Field Name:%s, %s -> %s,Permissions:%s, Groups:%s, Order:%s' % (
            self.workflow,
            self.source_state,
            self.destination_state,
            ','.join(self.permissions.values_list('name', flat=True)),
            ','.join(self.groups.values_list('name', flat=True)), self.priority)


def post_save_model(sender, instance, *args, **kwargs):
    parents = TransitionApprovalMeta.objects \
        .filter(workflow=instance.workflow, destination_state=instance.source_state) \
        .exclude(pk__in=instance.parents.values_list('pk', flat=True)) \
        .exclude(pk=instance.pk)

    children = TransitionApprovalMeta.objects \
        .filter(workflow=instance.workflow, source_state=instance.destination_state) \
        .exclude(parents__in=[instance.pk]) \
        .exclude(pk=instance.pk)

    instance = TransitionApprovalMeta.objects.get(pk=instance.pk)
    if parents:
        instance.parents.add(*parents)

    for child in children:
        child.parents.add(instance)


post_save.connect(post_save_model, sender=TransitionApprovalMeta)
