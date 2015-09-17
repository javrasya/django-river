from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from river.models import BaseModel

__author__ = 'ahmetdal'


class StateManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class State(BaseModel):
    class Meta:
        app_label = 'river'
        verbose_name = _("State")
        verbose_name_plural = _("States")

    objects = StateManager()

    slug = models.SlugField(unique=True, null=True, blank=True)
    label = models.CharField(max_length=50)
    description = models.CharField(_("Description"), max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.label

    def natural_key(self):
        return (self.slug,)

    def details(self):
        detail = super(State, self).details()
        detail.update(
            {
                'label': self.label,
                'description': self.description
            }
        )
        return detail
