from datetime import datetime, timedelta

from river.models import TransitionApproval, APPROVED, TransitionApprovalMeta
from river.tests.base_test import BaseTestCase
from river.tests.models.factories import TestModelObjectFactory
from river.tests.models.testmodel import TestModel
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


class RiverTest(BaseTestCase):

    def test_get_on_approval_objects(self):
        self.initialize_standard_scenario()
        objects = TestModelObjectFactory.create_batch(2)

        on_approval_objects = TestModel.river.my_field.get_on_approval_objects(as_user=self.user1)
        self.assertEqual(2, on_approval_objects.count())
        self.assertEqual(objects[0], on_approval_objects[0])

        on_approval_objects = TestModel.river.my_field.get_on_approval_objects(as_user=self.user2)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = TestModel.river.my_field.get_on_approval_objects(as_user=self.user3)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = TestModel.river.my_field.get_on_approval_objects(as_user=self.user4)
        self.assertEqual(0, on_approval_objects.count())

    def test_get_available_states(self):
        self.initialize_standard_scenario()
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
        self.initialize_standard_scenario()
        self.assertEqual(self.state1, TestModel.river.my_field.initial_state)

    def test_get_final_states(self):
        self.initialize_standard_scenario()
        self.assertListEqual([self.state41, self.state42, self.state51, self.state52], list(TestModel.river.my_field.final_states))

    def test_get_waiting_transition_approvals_without_skip(self):
        self.initialize_standard_scenario()
        object = TestModelObjectFactory.create_batch(1)[0]

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user1)
        self.assertEqual(1, transition_approvals.count())

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user2)
        self.assertEqual(0, transition_approvals.count())

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user3)
        self.assertEqual(0, transition_approvals.count())

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user4)
        self.assertEqual(0, transition_approvals.count())

    def test_get_waiting_transition_approvals_with_skip(self):
        self.initialize_standard_scenario()
        object = TestModelObjectFactory.create_batch(1)[0]

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user1)
        self.assertEqual(1, transition_approvals.count())
        self.assertEqual(self.state2, transition_approvals[0].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state2
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user2)
        self.assertEqual(1, transition_approvals.count())
        self.assertEqual(self.state3, transition_approvals[0].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state3
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user4)
        self.assertEqual(2, transition_approvals.count())
        self.assertEqual(self.state4, transition_approvals[0].destination_state)
        self.assertEqual(self.state5, transition_approvals[1].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state=self.state4
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user4)
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

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user4)
        self.assertEqual(3, transition_approvals.count())
        self.assertEqual(self.state4, transition_approvals[0].destination_state)
        self.assertEqual(self.state51, transition_approvals[1].destination_state)
        self.assertEqual(self.state52, transition_approvals[2].destination_state)

        TransitionApproval.objects.filter(
            workflow_object=object,
            field_name="my_field",
            destination_state__in=[self.state4, self.state5]
        ).update(skip=True)

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user4)
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

        transition_approvals = object.river.my_field.get_available_approvals(as_user=self.user4)
        self.assertEqual(2, transition_approvals.count())
        self.assertEqual(self.state42, transition_approvals[0].destination_state)
        self.assertEqual(self.state52, transition_approvals[1].destination_state)

    def test_proceed(self):
        self.initialize_standard_scenario()
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

    def test_cycle_proceedings(self):
        self.initialize_circular_scenario()
        object = TestModelObjectFactory.create_batch(1)[0]

        # No Cycle
        self.assertFalse(object.river.my_field._cycle_proceedings())
        object.river.my_field.approve(as_user=self.user1, next_state=self.in_progress_state, god_mod=True)
        self.assertEqual(5, TransitionApproval.objects.filter(object_id=object.pk).count())

        # No Cycle
        self.assertFalse(object.river.my_field._cycle_proceedings())
        object.river.my_field.approve(as_user=self.user2, next_state=self.resolved_state, god_mod=True)
        self.assertEqual(5, TransitionApproval.objects.filter(object_id=object.pk).count())

        # State is re-opened and cycle is detected. Transition in-progress to resolved proceeding is cloned
        self.assertFalse(object.river.my_field._cycle_proceedings())
        object.river.my_field.approve(as_user=self.user3, next_state=self.re_opened_state, god_mod=True)
        self.assertEqual(6, TransitionApproval.objects.filter(object_id=object.pk).count())

        self.assertEqual(TransitionApprovalMeta.objects.get(source_state=self.in_progress_state, destination_state=self.resolved_state),
                         TransitionApproval.objects.filter(object_id=object.pk).latest('date_created').meta)

        # There will be no cycling even if the method is invoked. Because cycling is done in proceeding.
        self.assertFalse(object.river.my_field._cycle_proceedings())
        self.assertEqual(6, TransitionApproval.objects.filter(object_id=object.pk).count())

        # State is in-progress and cycle is detected. Transition resolved to re-opened proceeding is cloned
        object.river.my_field.approve(as_user=self.user3, next_state=self.in_progress_state, god_mod=True)
        self.assertEqual(7, TransitionApproval.objects.filter(object_id=object.pk).count())
        self.assertEqual(TransitionApprovalMeta.objects.get(source_state=self.resolved_state, destination_state=self.re_opened_state),
                         TransitionApproval.objects.filter(object_id=object.pk).latest('date_created').meta)

        # State is resolved and cycle is detected. Transition re-opened to in-progress proceeding is cloned
        object.river.my_field.approve(as_user=self.user3, next_state=self.resolved_state, god_mod=True)
        self.assertEqual(8, TransitionApproval.objects.filter(object_id=object.pk).count())
        self.assertEqual(TransitionApprovalMeta.objects.get(source_state=self.re_opened_state, destination_state=self.in_progress_state),
                         TransitionApproval.objects.filter(object_id=object.pk).latest('date_created').meta)

        # State is re-opened and cycle is detected. Transition  in-progress to resolved proceeding is cloned
        self.assertFalse(object.river.my_field._cycle_proceedings())
        object.river.my_field.approve(as_user=self.user3, next_state=self.re_opened_state, god_mod=True)
        self.assertEqual(9, TransitionApproval.objects.filter(object_id=object.pk).count())
        self.assertEqual(TransitionApprovalMeta.objects.get(source_state=self.in_progress_state, destination_state=self.resolved_state),
                         TransitionApproval.objects.filter(object_id=object.pk).latest('date_created').meta)

        # State is in-progress and cycle is detected. Transition resolved to re-opened proceeding is cloned
        object.river.my_field.approve(as_user=self.user3, next_state=self.in_progress_state, god_mod=True)
        self.assertEqual(10, TransitionApproval.objects.filter(object_id=object.pk).count())
        self.assertEqual(TransitionApprovalMeta.objects.get(source_state=self.resolved_state, destination_state=self.re_opened_state),
                         TransitionApproval.objects.filter(object_id=object.pk).latest('date_created').meta)

        # State is resolved and cycle is detected. Transition re-opened to in-progress proceeding is cloned
        object.river.my_field.approve(as_user=self.user3, next_state=self.resolved_state, god_mod=True)
        self.assertEqual(11, TransitionApproval.objects.filter(object_id=object.pk).count())
        self.assertEqual(TransitionApprovalMeta.objects.get(source_state=self.re_opened_state, destination_state=self.in_progress_state),
                         TransitionApproval.objects.filter(object_id=object.pk).latest('date_created').meta)

        # No Cycle for closed state.
        object.river.my_field.approve(as_user=self.user4, next_state=self.closed_state, god_mod=True)
        self.assertEqual(11, TransitionApproval.objects.filter(object_id=object.pk).count())

    def test_get_waiting_approvals_slowness_test(self):
        self.initialize_standard_scenario()
        self.objects = TestModelObjectFactory.create_batch(100)
        before = datetime.now()
        for o in self.objects:
            o.river.my_field.get_available_states(as_user=self.user1)
        after = datetime.now()
        self.assertLess(after - before, timedelta(seconds=2))
