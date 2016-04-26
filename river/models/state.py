from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from river.models.base_model import BaseModel
from river.models.managers.state import StateManager

__author__ = 'ahmetdal'


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


def on_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.label)
    else:
        # To be sure it is slug
        instance.slug = slugify(instance.slug)


pre_save.connect(on_pre_save, State)
