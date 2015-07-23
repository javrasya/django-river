from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from river.models import BaseModel

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Application(BaseModel):
    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")

    name = models.CharField(_('Name'), max_length=200, null=True, blank=True)
    description = models.CharField(_("Description"), max_length=200, null=True, blank=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('Owner'), related_name='applications')

    def __unicode__(self):
        return self.name
