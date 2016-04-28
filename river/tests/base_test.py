import factory
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from river.tests.models import TestModel
from river.tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        print('%s is initialized' % self.__class__)

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        print('%s is finished' % self.__class__)

    def initialize_normal_scenario(self):
        from river.models.factories import \
            TransitionObjectFactory, \
            UserObjectFactory, \
            PermissionObjectFactory, \
            ProceedingMetaObjectFactory, \
            StateObjectFactory

        TransitionObjectFactory.reset_sequence(0)
        ProceedingMetaObjectFactory.reset_sequence(0)
        StateObjectFactory.reset_sequence(0)
        TestModel.objects.all().delete()

        self.content_type = ContentType.objects.get_for_model(TestModel)
        self.permissions = PermissionObjectFactory.create_batch(4)
        self.user1 = UserObjectFactory(user_permissions=[self.permissions[0]])
        self.user2 = UserObjectFactory(user_permissions=[self.permissions[1]])
        self.user3 = UserObjectFactory(user_permissions=[self.permissions[2]])
        self.user4 = UserObjectFactory(user_permissions=[self.permissions[3]])

        self.field = 'my_field'
        self.states = StateObjectFactory.create_batch(
            9,
            label=factory.Sequence(
                lambda n: "s%s" % str(n + 1) if n <= 4 else ("s4.%s" % str(n - 4) if n <= 6 else "s5.%s" % str(n - 6)))
        )
        self.transitions = TransitionObjectFactory.create_batch(8,
                                                                source_state=factory.Sequence(
                                                                    lambda n: self.states[n] if n <= 2 else (
                                                                        self.states[n - 1]) if n <= 4 else (
                                                                        self.states[n - 2] if n <= 6 else self.states[
                                                                            4])),
                                                                destination_state=factory.Sequence(
                                                                    lambda n: self.states[n + 1]))

        self.proceeding_metas = ProceedingMetaObjectFactory.create_batch(
            9,
            content_type=self.content_type,
            field=self.field,
            transition=factory.Sequence(lambda n: self.transitions[n] if n <= 1 else self.transitions[n - 1]),
            order=factory.Sequence(lambda n: 1 if n == 2 else 0)
        )

        for n, proceeding_meta in enumerate(self.proceeding_metas):
            proceeding_meta.permissions.add(self.permissions[n] if n <= 3 else self.permissions[3])

        self.objects = TestModelObjectFactory.create_batch(2)

    def initialize_circular_scenario(self):
        from river.models.factories import \
            TransitionObjectFactory, \
            UserObjectFactory, \
            PermissionObjectFactory, \
            ProceedingMetaObjectFactory, \
            StateObjectFactory

        TransitionObjectFactory.reset_sequence(0)
        ProceedingMetaObjectFactory.reset_sequence(0)
        StateObjectFactory.reset_sequence(0)
        TestModel.objects.all().delete()

        self.content_type = ContentType.objects.get_for_model(TestModel)
        self.permissions = PermissionObjectFactory.create_batch(4)
        self.user1 = UserObjectFactory(user_permissions=[self.permissions[0]])
        self.user2 = UserObjectFactory(user_permissions=[self.permissions[1]])
        self.user3 = UserObjectFactory(user_permissions=[self.permissions[2]])
        self.user4 = UserObjectFactory(user_permissions=[self.permissions[3]])

        self.field = 'my_field'

        self.open_state = StateObjectFactory(
            label='open'
        )
        self.in_progress_state = StateObjectFactory(
            label='in-progress'
        )

        self.resolved_state = StateObjectFactory(
            label='resolved'
        )
        self.re_opened_state = StateObjectFactory(
            label='re-opened'
        )

        self.closed_state = StateObjectFactory(
            label='closed'
        )

        self.transitions = [
            TransitionObjectFactory(source_state=self.open_state, destination_state=self.in_progress_state),
            TransitionObjectFactory(source_state=self.in_progress_state,
                                    destination_state=self.resolved_state),
            TransitionObjectFactory(source_state=self.resolved_state,
                                    destination_state=self.re_opened_state),
            TransitionObjectFactory(source_state=self.resolved_state, destination_state=self.closed_state),
            TransitionObjectFactory(source_state=self.re_opened_state, destination_state=self.in_progress_state)]

        self.proceeding_metas = ProceedingMetaObjectFactory.create_batch(
            5,
            content_type=self.content_type,
            field=self.field,
            transition=factory.Sequence(lambda n: self.transitions[n]),
            order=0
        )

        for n, proceeding_meta in enumerate(self.proceeding_metas):
            proceeding_meta.permissions.add(self.permissions[n] if n < len(self.permissions) else self.permissions[0])

        self.objects = TestModelObjectFactory.create_batch(2)
