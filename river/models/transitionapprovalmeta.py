from __future__ import unicode_literals

from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from river.config import app_config
from river.models import State
from river.models.base_model import BaseModel
from river.models.managers.transitionmetada import TransitionApprovalMetadataManager

__author__ = 'ahmetdal'

BACKWARD = 0
FORWARD = 1

DIRECTIONS = [
    (BACKWARD, _("Backward")),
    (FORWARD, _("Forward"))
]


@python_2_unicode_compatible
class TransitionApprovalMeta(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Transition Approval Meta")
        verbose_name_plural = _("Transition Approval Meta")
        unique_together = [('content_type', 'field_name', 'source_state', 'destination_state', 'priority')]

    objects = TransitionApprovalMetadataManager()

    content_type = models.ForeignKey(app_config.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'), on_delete=CASCADE)
    field_name = models.CharField(_("Field Name"), max_length=200)

    # transition = models.ForeignKey(Transition, verbose_name=_('Transition'), on_delete=CASCADE)
    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transition_approval_meta_as_source', on_delete=CASCADE)
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"), related_name='transition_approval_meta_as_destination', on_delete=CASCADE)
    # direction = models.SmallIntegerField(_("Transition Direction"), choices=DIRECTIONS, default=FORWARD)

    permissions = models.ManyToManyField(app_config.PERMISSION_CLASS, verbose_name=_('Permissions'), blank=True)
    groups = models.ManyToManyField(app_config.GROUP_CLASS, verbose_name=_('Groups'), blank=True)
    priority = models.IntegerField(default=0, verbose_name=_('Priority'), null=True)
    action_text = models.TextField(_("Action Text"), max_length=200, null=True, blank=True)
    parents = models.ManyToManyField('self', verbose_name='parents', related_name='children', symmetrical=False, db_index=True, blank=True)

    def natural_key(self):
        return self.field_name, self.content_type, self.source_state, self.destination_state, self.priority

    def __str__(self):
        return 'Field Name:%s, %s -> %s,Permissions:%s, Groups:%s, Order:%s' % (
            self.field_name,
            self.source_state,
            self.destination_state,
            ','.join(self.permissions.values_list('name', flat=True)),
            ','.join(self.groups.values_list('name', flat=True)), self.priority)


#
#
# def post_group_change(sender, instance, *args, **kwargs):
#     from river.services.proceeding import ProceedingService
#     from river.models.proceeding import PENDING
#
#     for proceeding_pending in instance.proceedings.filter(status=PENDING):
#         ProceedingService.override_groups(proceeding_pending, instance.groups.all())
#
#
# def post_permissions_change(sender, instance, *args, **kwargs):
#     from river.models.proceeding import PENDING
#     from river.services.proceeding import ProceedingService
#
#     for proceeding_pending in instance.proceedings.filter(status=PENDING):
#         ProceedingService.override_permissions(proceeding_pending, instance.permissions.all())


def post_save_model(sender, instance, *args, **kwargs):
    parents = TransitionApprovalMeta.objects \
        .filter(field_name=instance.field_name, destination_state=instance.source_state) \
        .exclude(pk__in=instance.parents.values_list('pk', flat=True)) \
        .exclude(pk=instance.pk)

    children = TransitionApprovalMeta.objects \
        .filter(field_name=instance.field_name, source_state=instance.destination_state) \
        .exclude(parents__in=[instance.pk]) \
        .exclude(pk=instance.pk)

    instance = TransitionApprovalMeta.objects.get(pk=instance.pk)
    if parents:
        instance.parents.add(*parents)

    for child in children:
        child.parents.add(instance)


# m2m_changed.connect(post_group_change, sender=TransitionApprovalMeta.groups.through)
# m2m_changed.connect(post_permissions_change, sender=TransitionApprovalMeta.permissions.through)

post_save.connect(post_save_model, sender=TransitionApprovalMeta)
