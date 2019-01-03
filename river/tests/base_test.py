from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from river.models.factories import StateObjectFactory, TransitionApprovalMetaFactory, PermissionObjectFactory, UserObjectFactory
from river.tests.models import TestModel

__author__ = 'ahmetdal'


class BaseTestCase(TestCase):
    def initialize_standard_scenario(self):
        TransitionApprovalMetaFactory.reset_sequence(0)
        StateObjectFactory.reset_sequence(0)

        content_type = ContentType.objects.get_for_model(TestModel)
        permissions = PermissionObjectFactory.create_batch(4)
        self.user1 = UserObjectFactory(user_permissions=[permissions[0]])
        self.user2 = UserObjectFactory(user_permissions=[permissions[1]])
        self.user3 = UserObjectFactory(user_permissions=[permissions[2]])
        self.user4 = UserObjectFactory(user_permissions=[permissions[3]])

        self.state1 = StateObjectFactory(label="state1")
        self.state2 = StateObjectFactory(label="state2")
        self.state3 = StateObjectFactory(label="state3")
        self.state4 = StateObjectFactory(label="state4")
        self.state5 = StateObjectFactory(label="state5")

        self.state41 = StateObjectFactory(label="state4.1")
        self.state42 = StateObjectFactory(label="state4.2")

        self.state51 = StateObjectFactory(label="state5.1")
        self.state52 = StateObjectFactory(label="state5.2")

        t1 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state1,
            destination_state=self.state2,
            priority=0
        )
        t1.permissions.add(permissions[0])

        t2 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state2,
            destination_state=self.state3,
            priority=0
        )
        t2.permissions.add(permissions[1])

        t3 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state2,
            destination_state=self.state3,
            priority=1
        )
        t3.permissions.add(permissions[2])

        t4 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state3,
            destination_state=self.state4,
            priority=0
        )
        t4.permissions.add(permissions[3])

        t5 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state3,
            destination_state=self.state5,
            priority=0
        )
        t5.permissions.add(permissions[3])

        t6 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state4,
            destination_state=self.state41,
            priority=0
        )
        t6.permissions.add(permissions[3])

        t7 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state4,
            destination_state=self.state42,
            priority=0
        )
        t7.permissions.add(permissions[3])

        t8 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state5,
            destination_state=self.state51,
            priority=0
        )
        t8.permissions.add(permissions[3])

        t9 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.state5,
            destination_state=self.state52,
            priority=0
        )
        t9.permissions.add(permissions[3])

    def initialize_circular_scenario(self):
        StateObjectFactory.reset_sequence(0)
        TransitionApprovalMetaFactory.reset_sequence(0)

        content_type = ContentType.objects.get_for_model(TestModel)
        permissions = PermissionObjectFactory.create_batch(4)
        self.user1 = UserObjectFactory(user_permissions=[permissions[0]])
        self.user2 = UserObjectFactory(user_permissions=[permissions[1]])
        self.user3 = UserObjectFactory(user_permissions=[permissions[2]])
        self.user4 = UserObjectFactory(user_permissions=[permissions[3]])

        self.open_state = StateObjectFactory(label='open')
        self.in_progress_state = StateObjectFactory(label='in-progress')
        self.resolved_state = StateObjectFactory(label='resolved')
        self.re_opened_state = StateObjectFactory(label='re-opened')
        self.closed_state = StateObjectFactory(label='closed')

        t1 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.open_state,
            destination_state=self.in_progress_state,
        )
        t1.permissions.add(permissions[0])

        t2 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.in_progress_state,
            destination_state=self.resolved_state,
        )
        t2.permissions.add(permissions[1])

        t3 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.resolved_state,
            destination_state=self.re_opened_state,
        )
        t3.permissions.add(permissions[2])

        t4 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.resolved_state,
            destination_state=self.closed_state,
        )
        t4.permissions.add(permissions[3])

        t5 = TransitionApprovalMetaFactory.create(
            field_name="my_field",
            content_type=content_type,
            source_state=self.re_opened_state,
            destination_state=self.in_progress_state,
        )
        t5.permissions.add(permissions[0])
