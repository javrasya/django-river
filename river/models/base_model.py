from django.conf import settings

from django.db import models

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def details(self):
        return {'pk': self.pk}

    def authenticate_header(self, request):
        return None
