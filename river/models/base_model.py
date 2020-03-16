from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _

from river.models.managers.rivermanager import RiverManager

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class BaseModel(models.Model):
    objects = RiverManager()

    date_created = models.DateTimeField(_('Date Created'), null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(_('Date Updated'), null=True, blank=True, auto_now=True)

    class Meta:
        app_label = 'river'
        abstract = True

    def details(self):
        return {'pk': self.pk}
