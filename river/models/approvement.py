try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from django.db import models

from django.utils.translation import ugettext_lazy as _

from river.models.approvement_meta import ApprovementMeta
from river.models.base_model import BaseModel
from river.models.managers.approvement import ApprovementManager
from river.services.config import RiverConfig

__author__ = 'ahmetdal'

PENDING = 0
APPROVED = 1
REJECTED = 2

APPROVEMENT_STATUSES = [
    (PENDING, _('Pending')),
    (APPROVED, _('Approved')),
    (REJECTED, _('Rejected')),
]


class Approvement(BaseModel):
    class Meta:
        verbose_name = _("Approvement")
        verbose_name_plural = _("Approvements")

    objects = ApprovementManager()

    content_type = models.ForeignKey(RiverConfig.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(verbose_name=_('Related Object'))
    field = models.CharField(verbose_name=_('Field'), max_length=200)
    workflow_object = GenericForeignKey('content_type', 'object_id')

    meta = models.ForeignKey(ApprovementMeta, verbose_name=_('Approve Definition'), related_name="approvements")
    transactioner = models.ForeignKey(RiverConfig.USER_CLASS, verbose_name=_('Approver'), null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(_('Status'), choices=APPROVEMENT_STATUSES, default=PENDING)

    skip = models.BooleanField(_('Skip'), default=False)

    permissions = models.ManyToManyField(RiverConfig.PERMISSION_CLASS, verbose_name=_('Permissions'))
    groups = models.ManyToManyField(RiverConfig.GROUP_CLASS, verbose_name=_('Groups'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    enabled = models.BooleanField(_('Enabled?'), default=True)
