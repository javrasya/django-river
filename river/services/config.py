from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

__author__ = 'ahmetdal'


class RiverConfig:
    EMBEDDED = settings.get('RIVER_IS_EMBEDDED', True)
    CONTENT_TYPE_CLASS = settings.get('RIVER_CONTENT_TYPE_CLASS', ContentType)
    USER_CLASS = settings.get('RIVER_USER_CLASS', User)
    PERMISSION_CLASS = settings.get('RIVER_PERMISSION_CLASS', Permission)
    GROUP_CLASS = settings.get('RIVER_GROUP_CLASS', Group)
