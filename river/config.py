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
        self.HOOKING_BACKEND = getattr(settings, self.get_with_prefix('HOOKING_BACKEND'), {'backend': 'river.hooking.backends.database.DatabaseHookingBackend'})

        # Generated
        self.HOOKING_BACKEND_CLASS = self.HOOKING_BACKEND.get('backend')
        self.HOOKING_BACKEND_CONFIG = self.HOOKING_BACKEND.get('config', {})


app_config = RiverConfig()
app_config.load()
