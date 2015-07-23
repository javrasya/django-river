from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.approvement_meta import ApprovementMeta
from river.models.base_model import BaseModel
from river.models.field import Field
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

    content_type = models.ForeignKey(RiverConfig.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(verbose_name=_('Related Object'))
    field = models.ForeignKey(Field, verbose_name=_('Field'))
    # object = generic.GenericForeignKey('content_type', 'object_pk')

    meta = models.ForeignKey(ApprovementMeta, verbose_name=_('Approve Definition'))
    transactioner = models.ForeignKey(RiverConfig.USER_CLASS, verbose_name=_('Approver'), null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(_('Status'), choices=APPROVEMENT_STATUSES, default=PENDING)

    skip = models.BooleanField(_('Skip'), default=False)

    permissions = models.ManyToManyField(RiverConfig.PERMISSION_CLASS, verbose_name=_('Permissions'), null=True)
    groups = models.ManyToManyField(RiverConfig.GROUP_CLASS, verbose_name=_('Groups'), null=True)
