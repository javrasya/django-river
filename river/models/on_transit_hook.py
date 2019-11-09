from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _

from river.models import State
from river.models.hook import Hook


class OnTransitHook(Hook):
    class Meta:
        unique_together = [('callback_function', 'workflow', 'source_state', 'destination_state', 'content_type', 'object_id', 'iteration')]

    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='on_transition_hook_as_source', on_delete=CASCADE)
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"), related_name='on_transition_hook_as_destination', on_delete=CASCADE)
    iteration = models.IntegerField(default=0, verbose_name=_('Priority'), null=True, blank=True)
