from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

__author__ = 'ahmetdal'


class RiverConfig(object):
    # from settings
    prefix = 'RIVER'

    def get_with_prefix(self, config):
        return '%s_%s' % (self.prefix, config)

    def __getattr__(self, item):
        from django.conf import settings
        allowed_configurations = {
            'CONTENT_TYPE_CLASS': ContentType,
            'USER_CLASS': settings.AUTH_USER_MODEL,
            'PERMISSION_CLASS': Permission,
            'GROUP_CLASS': Group,
            'INJECT_MODEL_ADMIN': False
        }
        if item in allowed_configurations.keys():
            default_value = allowed_configurations[item]
            return getattr(settings, self.get_with_prefix(item), default_value)
        else:
            raise AttributeError(item)


app_config = RiverConfig()
