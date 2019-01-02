from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from river.models import TransitionApproval, APPROVED
from river.models.factories import StateObjectFactory, TransitionApprovalMetaFactory, UserObjectFactory, PermissionObjectFactory
from river.tests.models.factories import TestModelObjectFactory
from river.tests.models.testmodel import TestModel
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


class RiverTest(TestCase):

    def setUp(self):
        self.initialize_advance_scenario()

    def test_get_objects_waiting_for_approval_for_user(self):
        objects = TestModelObjectFactory.create_batch(2)

        on_approval_objects = TestModel.river.my_field.get_objects_waiting_for_approval(as_user=self.user1)
        self.assertEqual(2, on_approval_objects.count())
        self.assertEqual(objects[0], on_approval_objects[0])

        on_approval_objects = TestModel.river.my_field.get_objects_waiting_for_approval(as_user=self.user2)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = TestModel.river.my_field.get_objects_waiting_for_approval(as_user=self.user3)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = TestModel.river.my_field.get_objects_waiting_for_approval(as_user=self.user4)
        self.assertEqual(0, on_approval_objects.count())

    def test_get_available_states(self):
        object = TestModelObjectFactory.create_batch(1)[0]
        available_states = object.river.my_field.get_available_states()
        self.assertEqual(1, available_states.count())
        self.assertEqual(self.state2, available_states[0])

        available_states = object.river.my_field.get_available_states(as_user=self.user1)
        self.assertEqual(1, available_states.count())
        self.assertEqual(self.state2, available_states[0])

        available_states = object.river.my_field.get_available_states(as_user=self.user2)
        self.assertEqual(0, available_states.count())

        available_states = object.river.my_field.get_available_states(as_user=self.user3)
        self.assertEqual(0, available_states.count())

        available_states = object.river.my_field.get_available_states(as_user=self.user4)
        self.assertEqual(0, available_states.count())

    def test_get_initial_state(self):
        self.assertEqual(self.state1, TestModel.river.my_field.initial_state)

    def test_get_final_states(self):
        self.assertListEqual([self.state41, self.state42, self.state51, self.state52], list(TestModel.river.my_field.final_states))

    def test_get_waiting_transition_approvals_without_skip(self):
        object = TestModelObjectFactory.create_batch(1)[0]

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user1)
        self.assertEqual(1, transition_approvals.count())

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user2)
        self.assertEqual(0, transition_approvals.count())

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user3)
        self.assertEqual(0, transition_approvals.count())

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user4)
        self.assertEqual(0, transition_approvals.count())

    def test_get_waiting_transition_approvals_with_skip(self):
        object = TestModelObjectFactory.create_batch(1)[0]

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user1)
        self.assertEqual(1, transition_approvals.count())
        self.assertEqual(self.state2, transition_approvals[0].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state2
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user2)
        self.assertEqual(1, transition_approvals.count())
        self.assertEqual(self.state3, transition_approvals[0].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state3
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user4)
        self.assertEqual(2, transition_approvals.count())
        self.assertEqual(self.state4, transition_approvals[0].destination_state)
        self.assertEqual(self.state5, transition_approvals[1].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state4
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user4)
        self.assertEqual(3, transition_approvals.count())
        self.assertEqual(self.state5, transition_approvals[0].destination_state)
        self.assertEqual(self.state41, transition_approvals[1].destination_state)
        self.assertEqual(self.state42, transition_approvals[2].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state4
        ).update(skip=False)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state5
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user4)
        self.assertEqual(3, transition_approvals.count())
        self.assertEqual(self.state4, transition_approvals[0].destination_state)
        self.assertEqual(self.state51, transition_approvals[1].destination_state)
        self.assertEqual(self.state52, transition_approvals[2].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state__in=[self.state4, self.state5]
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user4)
        self.assertEqual(4, transition_approvals.count())
        self.assertEqual(self.state41, transition_approvals[0].destination_state)
        self.assertEqual(self.state42, transition_approvals[1].destination_state)
        self.assertEqual(self.state51, transition_approvals[2].destination_state)
        self.assertEqual(self.state52, transition_approvals[3].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state__in=[self.state41, self.state51]
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_transition_approvals(as_user=self.user4)
        self.assertEqual(2, transition_approvals.count())
        self.assertEqual(self.state42, transition_approvals[0].destination_state)
        self.assertEqual(self.state52, transition_approvals[1].destination_state)

    def test_proceed(self):
        object = TestModelObjectFactory.create_batch(1)[0]

        # ####################
        # STATE 1 - STATE 2
        # Only User1(2001) can proceed and after his proceed state must be changed to STATE 2
        # ###################

        # Proceeded by user has no required permission for this transition

        try:
            object.river.my_field.approve(as_user=self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            object.river.my_field.approve(as_user=self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            object.river.my_field.approve(as_user=self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        self.assertEqual(self.state1, object.my_field)

        object.river.my_field.approve(as_user=self.user1)

        self.assertEqual(self.state2, object.my_field)

        transition_approvals = TransitionApproval.objects.filter(
            workflow_object=object,
            status=APPROVED,
            source_state=self.state1,
            destination_state=self.state2
        )
        self.assertEqual(1, transition_approvals.count())
        self.assertIsNotNone(transition_approvals[0].transactioner)
        self.assertEqual(self.user1, transition_approvals[0].transactioner)
        self.assertIsNotNone(transition_approvals[0].transaction_date)

        # ####################
        # STATE 2 - STATE 3
        # User2(2002) is first proceeder and User3(2003) is second proceeder. This must be done with turn. After proceeding is done, state is gonna be changed to STATE 3
        # ####################

        # Proceeded by user has no required permission for this transition
        try:
            object.river.my_field.approve(as_user=self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            object.river.my_field.approve(as_user=self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Turn is User2(2002)s, not User3(2003)s. After User2(2002) proceeded, User3(2003) can proceed.
        try:
            object.river.my_field.approve(as_user=self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Proceeded by two user has required permission for this transition to get next state (order is user2(2002),user3(2003)).
        object.river.my_field.approve(as_user=self.user2)
        self.assertEqual(self.state2, object.my_field)

        transition_approvals = TransitionApproval.objects.filter(
            workflow_object=object,
            status=APPROVED,
            source_state=self.state2,
            destination_state=self.state3
        )
        self.assertEqual(1, transition_approvals.count())
        self.assertIsNotNone(transition_approvals[0].transactioner)
        self.assertEqual(self.user2, transition_approvals[0].transactioner)
        self.assertIsNotNone(transition_approvals[0].transaction_date)

        try:
            object.river.my_field.approve(as_user=self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

            object.river.my_field.approve(as_user=self.user3)
        self.assertEqual(self.state3, object.my_field)

        transition_approvals = TransitionApproval.objects.filter(
            workflow_object=object,
            status=APPROVED,
            source_state=self.state2,
            destination_state=self.state3
        )
        self.assertEqual(2, transition_approvals.count())
        self.assertIsNotNone(transition_approvals[0].transactioner)
        self.assertIsNotNone(transition_approvals[1].transactioner)
        self.assertEqual(self.user2, transition_approvals[0].transactioner)
        self.assertEqual(self.user3, transition_approvals[1].transactioner)
        self.assertIsNotNone(transition_approvals[0].transaction_date)
        self.assertIsNotNone(transition_approvals[1].transaction_date)

        # ####################
        # STATE 3 - STATE 4 or STATE 5
        # Only User4(2004) can proceed by giving the exact next state and after his proceed with his state must be changed to STATE 4 or STATE 5
        # ###################

        # Proceeded by user has no required permission for this transition
        try:
            object.river.my_field.approve(as_user=self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Proceeded by user has no required permission for this transition
        try:
            object.river.my_field.approve(as_user=self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Proceeded by user has no required permission for this transition
        try:
            object.river.my_field.approve(as_user=self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # There are STATE 4 and STATE 5 as next. State must be given to switch
        try:
            object.river.my_field.approve(as_user=self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'State must be given when there are multiple states for destination')
            self.assertEqual(ErrorCode.NEXT_STATE_IS_REQUIRED, e.code)

        # There are STATE 4 and STATE 5 as next. State among STATE 4 and STATE 5 must be given to switch, not other state
        try:
            object.river.my_field.approve(as_user=self.user4, next_state=self.state3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e),
                             "Invalid state is given(%s). Valid states is(are) %s" % (
                                 self.state3.__str__(), ','.join([ast.__str__() for ast in [self.state4, self.state5]])))
            self.assertEqual(ErrorCode.INVALID_NEXT_STATE_FOR_USER, e.code)

        # There are STATE 4 and STATE 5 as next. After one of them is given to proceeding, the state must be switch to it immediately.
        object.river.my_field.approve(as_user=self.user4, next_state=self.state5)
        self.assertEqual(self.state5, object.my_field)

        transition_approvals = TransitionApproval.objects.filter(
            workflow_object=object,
            status=APPROVED,
            source_state=self.state3,
            destination_state=self.state5
        )
        self.assertEqual(1, transition_approvals.count())
        self.assertIsNotNone(transition_approvals[0].transactioner)
        self.assertEqual(self.user4, transition_approvals[0].transactioner)
        self.assertIsNotNone(transition_approvals[0].transaction_date)

    def initialize_advance_scenario(self):
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
