from mptt.fields import TreeOneToOneField

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.proceeding_meta import ProceedingMeta
from river.models.base_model import BaseModel
from river.models.managers.proceeding import ProceedingManager
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


class Proceeding(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Proceeding")
        verbose_name_plural = _("Proceedings")

    objects = ProceedingManager()

    content_type = models.ForeignKey(app_config.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(verbose_name=_('Related Object'))
    field = models.CharField(verbose_name=_('Field'), max_length=200)
    workflow_object = GenericForeignKey('content_type', 'object_id')

    meta = models.ForeignKey(ProceedingMeta, verbose_name=_('Meta'), related_name="proceedings")
    transactioner = models.ForeignKey(app_config.USER_CLASS, verbose_name=_('Transactioner'), null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(_('Status'), choices=PROCEEDING_STATUSES, default=PENDING)

    skip = models.BooleanField(_('Skip'), default=False)

    permissions = models.ManyToManyField(app_config.PERMISSION_CLASS, verbose_name=_('Permissions'))
    groups = models.ManyToManyField(app_config.GROUP_CLASS, verbose_name=_('Groups'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    enabled = models.BooleanField(_('Enabled?'), default=True)

    previous = TreeOneToOneField("self", verbose_name=_('Previous Proceeding'), related_name="next_proceeding",
                                 null=True, blank=True)

    cloned = models.BooleanField(_('Cloned?'), default=False)
