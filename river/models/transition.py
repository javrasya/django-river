import logging

from django.db.models import CASCADE, PROTECT

from river.models import State, Workflow, TransitionMeta

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
CANCELLED = "cancelled"
JUMPED = "jumped"
DONE = "done"

STATUSES = [
    (PENDING, _('Pending')),
    (CANCELLED, _('Cancelled')),
    (DONE, _('Done')),
    (JUMPED, _('Jumped')),
]

LOGGER = logging.getLogger(__name__)


class Transition(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")

    objects = TransitionApprovalManager()
    content_type = models.ForeignKey(app_config.CONTENT_TYPE_CLASS, verbose_name=_('Content Type'), on_delete=CASCADE)
    object_id = models.CharField(max_length=50, verbose_name=_('Related Object'))
    workflow_object = GenericForeignKey('content_type', 'object_id')

    meta = models.ForeignKey(TransitionMeta, verbose_name=_('Meta'), related_name="transitions", on_delete=PROTECT)
    workflow = models.ForeignKey(Workflow, verbose_name=_("Workflow"), related_name='transitions', on_delete=PROTECT)
    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transition_as_source', on_delete=PROTECT)
    destination_state = models.ForeignKey(State, verbose_name=_("Destination State"), related_name='transition_as_destination', on_delete=PROTECT)

    status = models.CharField(_('Status'), choices=STATUSES, max_length=100, default=PENDING)

    iteration = models.IntegerField(default=0, verbose_name=_('Priority'))

    @property
    def next_transitions(self):
        return Transition.objects.filter(
            workflow=self.workflow,
            workflow_object=self.workflow_object,
            source_state=self.destination_state,
            iteration=self.iteration + 1
        )

    @property
    def peers(self):
        return Transition.objects.filter(
            workflow=self.workflow,
            workflow_object=self.workflow_object,
            source_state=self.source_state,
            iteration=self.iteration
        ).exclude(pk=self.pk)
