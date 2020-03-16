

from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from river.config import app_config


class RiverQuerySet(QuerySet):
    def first(self):
        if app_config.IS_MSSQL:
            return next(iter(self), None)
        else:
            return super(RiverQuerySet, self).first()


class RiverManager(BaseManager.from_queryset(RiverQuerySet)):
    pass
