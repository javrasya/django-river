import os
from os.path import dirname

import six
from django.db import connection
from django.contrib.auth.models import Permission

from river.driver.river_driver import RiverDriver
from river.models import TransitionApproval


class MsSqlDriver(RiverDriver):

    def __init__(self, *args, **kwargs):
        super(MsSqlDriver, self).__init__(*args, **kwargs)
        with open(os.path.join(dirname(dirname(__file__)), "sql", "mssql", "get_available_approvals.sql")) as f:
            self.available_approvals_sql_template = f.read().replace("river.dbo.", "")
        self.cursor = connection.cursor()

    def get_available_approvals(self, as_user):
        with connection.cursor() as cursor:
            cursor.execute(self._clean_sql % {
                "workflow_id": self.workflow.pk,
                "transactioner_id": as_user.pk,
                "field_name": self.field_name,
                "permission_ids": self._permission_ids_str(as_user),
                "group_ids": self._group_ids_str(as_user),
                "workflow_object_table": self.wokflow_object_class._meta.db_table,
                "object_pk_name": self.wokflow_object_class._meta.pk.name
            })

            return TransitionApproval.objects.filter(pk__in=[row[0] for row in cursor.fetchall()])

    @staticmethod
    def _permission_ids_str(as_user):
        permissions = as_user.user_permissions.all() | Permission.objects.filter(group__user=as_user)
        return ",".join(list(six.moves.map(str, permissions.values_list("pk", flat=True))) or ["-1"])

    @staticmethod
    def _group_ids_str(as_user):
        return ",".join(list(six.moves.map(str, as_user.groups.all().values_list("pk", flat=True))) or ["-1"])

    @property
    def _clean_sql(self):
        return self.available_approvals_sql_template \
            .replace("'%(workflow_id)s'", "%(workflow_id)s") \
            .replace("'%(transactioner_id)s'", "%(transactioner_id)s") \
            .replace("'%(field_name)s'", "%(field_name)s") \
            .replace("'%(permission_ids)s'", "%(permission_ids)s") \
            .replace("'%(group_ids)s'", "%(group_ids)s") \
            .replace("'%(workflow_object_table)s'", "%(workflow_object_table)s") \
            .replace("'%(object_pk_name)s'", "%(object_pk_name)s")
