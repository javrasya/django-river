from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

__author__ = 'ahmetdal'


class RiverConfig:
    # EMBEDDED = settings.get('RIVER_IS_EMBEDDED', True)
    CONTENT_TYPE_CLASS = getattr(settings, 'RIVER_CONTENT_TYPE_CLASS', ContentType)
    USER_CLASS = getattr(settings, 'RIVER_USER_CLASS', settings.AUTH_USER_MODEL)
    PERMISSION_CLASS = getattr(settings, 'RIVER_PERMISSION_CLASS', Permission)
    GROUP_CLASS = getattr(settings, 'RIVER_GROUP_CLASS', Group)
    HANDLER_BACKEND = getattr(settings, 'RIVER_HANDLER_BACKEND', {'backend': 'river.handlers.backends.memory.MemoryHandlerBackend'})
    HANDLER_BACKEND_CLASS = HANDLER_BACKEND.get('backend')
    HANDLER_BACKEND_CONFIG = HANDLER_BACKEND.get('config', {})
