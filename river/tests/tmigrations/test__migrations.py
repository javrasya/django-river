import os
import sqlite3
import sys
from unittest import skipUnless

from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction
from django.test.utils import override_settings
from hamcrest import assert_that, equal_to, has_length

from river.models.factories import StateObjectFactory, WorkflowFactory, TransitionApprovalMetaFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.core.management import call_command
from django.test import TestCase

_author_ = 'ahmetdal'


def clean_migrations():
    for f in os.listdir("river/tests/volatile/river/"):
        if f != "__init__.py" and f != "__pycache__":
            os.remove(os.path.join("river/tests/volatile/river/", f))

    for f in os.listdir("river/tests/volatile/river_tests/"):
        if f != "__init__.py" and f != "__pycache__":
            os.remove(os.path.join("river/tests/volatile/river_tests/", f))


class MigrationTests(TestCase):
    """
    This is the case to detect missing migration issues like https://github.com/javrasya/django-river/issues/30
    """

    migrations_before = []
    migrations_after = []

    def setUp(self):
        """
            Remove migration file generated by test if there is any missing.
        """
        clean_migrations()

    def tearDown(self):
        """
            Remove migration file generated by test if there is any missing.
        """
        clean_migrations()

    @override_settings(MIGRATION_MODULES={"river": "river.tests.volatile.river"})
    def test_shouldCreateAllMigrations(self):
        for f in os.listdir("river/migrations"):
            if f != "__init__.py" and f != "__pycache__" and not f.endswith(".pyc"):
                open(os.path.join("river/tests/volatile/river/", f), 'wb').write(open(os.path.join("river/migrations", f), 'rb').read())

        self.migrations_before = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/tests/volatile/river/')))

        out = StringIO()
        sys.stout = out

        call_command('makemigrations', 'river', stdout=out)

        self.migrations_after = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/tests/volatile/river/')))

        assert_that(out.getvalue(), equal_to("No changes detected in app 'river'\n"))
        assert_that(self.migrations_after, has_length(len(self.migrations_before)))

    @override_settings(MIGRATION_MODULES={"tests": "river.tests.volatile.river_tests"})
    def test__shouldNotKeepRecreatingMigrationsWhenNoChange(self):
        call_command('makemigrations', 'tests')

        self.migrations_before = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/tests/volatile/river_tests/')))

        out = StringIO()
        sys.stout = out

        call_command('makemigrations', 'tests', stdout=out)

        self.migrations_after = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/tests/volatile/river_tests/')))

        assert_that(out.getvalue(), equal_to("No changes detected in app 'tests'\n"))
        assert_that(self.migrations_after, has_length(len(self.migrations_before)))

    @override_settings(MIGRATION_MODULES={"tests": "river.tests.volatile.river_tests"})
    @skipUnless(sqlite3.sqlite_version <= "3.24.0", "This test is not able to run with newer version of sqlite")
    def test__shouldMigrateTransitionApprovalStatusToStringInDB(self):
        out = StringIO()
        sys.stout = out
        cur = connection.cursor()

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        workflow = WorkflowFactory(initial_state=state1, content_type=ContentType.objects.get_for_model(BasicTestModel), field_name="my_field")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0
        )
        workflow_object = BasicTestModelObjectFactory()

        result = cur.execute("select status from river_transitionapproval where object_id=%s;" % workflow_object.model.pk).fetchall()
        assert_that(result[0][0], equal_to("pending"))

        call_command('migrate', 'river', '0004', stdout=out)
        schema = cur.execute("PRAGMA table_info('river_transitionapproval');").fetchall()
        self.migrations_after = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/tests/volatile/river/')))
        status_col_type = list(filter(lambda column: column[1] == 'status', schema))[0][2]
        assert_that(status_col_type, equal_to("integer"))

        result = cur.execute("select status from river_transitionapproval where object_id=%s;" % workflow_object.model.pk).fetchall()
        assert_that(result[0][0], equal_to(0))

        call_command('migrate', 'river', stdout=out)
        schema = cur.execute("PRAGMA table_info('river_transitionapproval');").fetchall()

        self.migrations_after = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/tests/volatile/river/')))
        status_col_type = list(filter(lambda column: column[1] == 'status', schema))[0][2]
        assert_that(status_col_type, equal_to("varchar(100)"))

        result = cur.execute("select status from river_transitionapproval where object_id=%s;" % workflow_object.model.pk).fetchall()
        assert_that(result[0][0], equal_to("pending"))
