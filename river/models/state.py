from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.riverio.models.application_based import ApplicationBasedModel


__author__ = 'ahmetdal'


class State(ApplicationBasedModel):
    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")
        ordering = ('created_at',)

    label = models.CharField(max_length=50)
    description = models.CharField(_("Description"), max_length=200, null=True, blank=True)


    def __unicode__(self):
        return self.label


    def details(self):
        detail = super(State, self).details()
        detail.update(
            {
                'label': self.label,
                'description': self.description
            }
        )
        return detail





