from django.db.models import CASCADE
from mptt.fields import TreeOneToOneField

from river.models import State, TransitionApprovalMeta

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.managers.transitionapproval import TransitionApprovalManager
from river.config import app_config

__author__ = 'ahmetdal'

PENDING = 0
APPROVED = 1
REJECTED = 2

PROCEEDING_STATUSES = [
    (PENDING, _('Pending')),
    (APPROVED, _('Approved')),
    (REJECTED, _('Rejected')),
]


class TransitionApproval(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Transition Approval")
        verbose_name_plural = _("Transition Approvals")

    objects = TransitionApprovalManager()

    content_type = models.ForeignKey(app_config.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'), on_delete=CASCADE)
    field_name = models.CharField(_("Field Name"), max_length=200)

    object_id = models.CharField(max_length=50, verbose_name=_('Related Object'))
    workflow_object = GenericForeignKey('content_type', 'object_id')

    meta = models.ForeignKey(TransitionApprovalMeta, verbose_name=_('Meta'), related_name="proceedings", on_delete=CASCADE)
    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transition_approvals_as_source', on_delete=CASCADE)
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"), related_name='transition_approvals_as_destination', on_delete=CASCADE)

    transactioner = models.ForeignKey(app_config.USER_CLASS, verbose_name=_('Transactioner'), null=True, blank=True, on_delete=CASCADE)
    transaction_date = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(_('Status'), choices=PROCEEDING_STATUSES, default=PENDING)

    skip = models.BooleanField(_('Skip'), default=False)

    permissions = models.ManyToManyField(app_config.PERMISSION_CLASS, verbose_name=_('Permissions'))
    groups = models.ManyToManyField(app_config.GROUP_CLASS, verbose_name=_('Groups'))
    priority = models.IntegerField(default=0, verbose_name=_('Priority'))

    enabled = models.BooleanField(_('Enabled?'), default=True)

    previous = TreeOneToOneField("self", verbose_name=_('Previous Transition'), related_name="next_transition", null=True, blank=True, on_delete=CASCADE)

    cloned = models.BooleanField(_('Cloned?'), default=False)
