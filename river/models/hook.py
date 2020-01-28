import logging

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import PROTECT
from django.utils.translation import ugettext_lazy as _

from river.models import Workflow, GenericForeignKey, BaseModel
from river.models.function import Function

BEFORE = "BEFORE"
AFTER = "AFTER"

HOOK_TYPES = [
    (BEFORE, _('Before')),
    (AFTER, _('After')),
]

LOGGER = logging.getLogger(__name__)


class Hook(BaseModel):
    class Meta:
        abstract = True

    callback_function = models.ForeignKey(Function, verbose_name=_("Function"), related_name='%(app_label)s_%(class)s_hooks', on_delete=PROTECT)
    workflow = models.ForeignKey(Workflow, verbose_name=_("Workflow"), related_name='%(app_label)s_%(class)s_hooks', on_delete=PROTECT)

    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.CharField(max_length=200, blank=True, null=True)
    workflow_object = GenericForeignKey('content_type', 'object_id')

    hook_type = models.CharField(_('When?'), choices=HOOK_TYPES, max_length=50)

    def execute(self, context):
        try:
            self.callback_function.get()(context)
        except Exception as e:
            LOGGER.exception(e)
