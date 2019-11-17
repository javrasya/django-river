from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

__author__ = 'ahmetdal'


class RiverConfig(object):
    # from settings
    prefix = 'RIVER'

    def get_with_prefix(self, config):
        return '%s_%s' % (self.prefix, config)

    def load(self):
        self.CONTENT_TYPE_CLASS = getattr(settings, self.get_with_prefix('CONTENT_TYPE_CLASS'), ContentType)
        self.USER_CLASS = getattr(settings, self.get_with_prefix('USER_CLASS'), settings.AUTH_USER_MODEL)
        self.PERMISSION_CLASS = getattr(settings, self.get_with_prefix('PERMISSION_CLASS'), Permission)
        self.GROUP_CLASS = getattr(settings, self.get_with_prefix('GROUP_CLASS'), Group)
        self.INJECT_ADMIN = getattr(settings, self.get_with_prefix('INJECT_MODEL_ADMIN'), True)


app_config = RiverConfig()
app_config.load()
