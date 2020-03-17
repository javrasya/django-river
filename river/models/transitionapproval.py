import logging

from django.db.models import CASCADE, PROTECT, SET_NULL
from mptt.fields import TreeOneToOneField

from river.models import TransitionApprovalMeta, Workflow
from river.models.transition import Transition

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.managers.transitionapproval import TransitionApprovalManager
from river.config import app_config

PENDING = "pending"
APPROVED = "approved"
JUMPED = "jumped"
CANCELLED = "cancelled"

STATUSES = [
    (PENDING, _('Pending')),
    (APPROVED, _('Approved')),
    (CANCELLED, _('Cancelled')),
    (JUMPED, _('Jumped')),
]

LOGGER = logging.getLogger(__name__)


class TransitionApproval(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Transition Approval")
        verbose_name_plural = _("Transition Approvals")

    objects = TransitionApprovalManager()

    content_type = models.ForeignKey(app_config.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'), on_delete=CASCADE)

    object_id = models.CharField(max_length=50, verbose_name=_('Related Object'))
    workflow_object = GenericForeignKey('content_type', 'object_id')

    meta = models.ForeignKey(TransitionApprovalMeta, verbose_name=_('Meta'), related_name="transition_approvals", null=True, blank=True, on_delete=SET_NULL)
    workflow = models.ForeignKey(Workflow, verbose_name=_("Workflow"), related_name='transition_approvals', on_delete=PROTECT)

    transition = models.ForeignKey(Transition, verbose_name=_("Transition"), related_name='transition_approvals', on_delete=PROTECT)

    transactioner = models.ForeignKey(app_config.USER_CLASS, verbose_name=_('Transactioner'), null=True, blank=True, on_delete=SET_NULL)
    transaction_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(_('Status'), choices=STATUSES, max_length=100, default=PENDING)

    permissions = models.ManyToManyField(app_config.PERMISSION_CLASS, verbose_name=_('Permissions'))
    groups = models.ManyToManyField(app_config.GROUP_CLASS, verbose_name=_('Groups'))
    priority = models.IntegerField(default=0, verbose_name=_('Priority'))

    previous = TreeOneToOneField("self", verbose_name=_('Previous Transition'), related_name="next_transition", null=True, blank=True, on_delete=CASCADE)

    @property
    def peers(self):
        return TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            workflow=self.workflow,
            transition=self.transition,
        ).exclude(pk=self.pk)
