from river.models import State, Approvement, APPROVED

from river.services.object import ObjectService
from river.services.transition import TransitionService
from river.tests.services.approvement_service_based_test import ApprovementServiceBasedTest
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


class test__TransitionService(ApprovementServiceBasedTest):
    def test_approve_transition(self):

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)
        # ####################
        # STATE 1 - STATE 2
        # Only User1(2001) can approve and after his approve state must be changed to STATE 2
        # ###################

        # Approved by user has no required permission for this transition

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # Approved by user has no required permission for this transition

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # Approved by user has no required permission for this transition

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Approved by user has required permission for this transition

        self.assertEqual(State.objects.get(label='s1'), getattr(self.objects[0], self.field))

        TransitionService.approve_transition(self.objects[0], self.field, self.user1)

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))

        approvements = Approvement.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s1',
            meta__transition__destination_state__label='s2'
        )
        self.assertEqual(1, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertEqual(self.user1, approvements[0].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # ####################
        # STATE 2 - STATE 3
        # User2(2002) is first approver and User3(2003) is second approver. This must be done with turn. After approvement is done, state is gonna be changed to STATE 3
        # ####################

        # Approved by user has no required permission for this transition
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Approved by user has no required permission for this transition
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Turn is User2(2002)s, not User3(2003)s. After User2(2002) approved, User3(2003) can approve.
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # Approved by two user has required permission for this transition to get next state (order is user2(2002),user3(2003)).

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))
        TransitionService.approve_transition(self.objects[0], self.field, self.user2)

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))

        approvements = Approvement.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s2',
            meta__transition__destination_state__label='s3'
        )
        self.assertEqual(1, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertEqual(self.user2, approvements[0].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))

        TransitionService.approve_transition(self.objects[0], self.field, self.user3)

        self.assertEqual(State.objects.get(label='s3'), getattr(self.objects[0], self.field))

        approvements = Approvement.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s2',
            meta__transition__destination_state__label='s3'
        )
        self.assertEqual(2, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertIsNotNone(approvements[1].transactioner)
        self.assertEqual(self.user2, approvements[0].transactioner)
        self.assertEqual(self.user3, approvements[1].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)
        self.assertIsNotNone(approvements[1].transaction_date)

        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)



        # ####################
        # STATE 3 - STATE 4 or STATE 5
        # Only User4(2004) can approve by giving the exact next state and after his approve with his state must be changed to STATE 4 or STATE 5
        # ###################

        # Approved by user has no required permission for this transition
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Approved by user has no required permission for this transition
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Approved by user has no required permission for this transition
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # There are STATE 4 and STATE 5 as next. State must be given to switch
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'State must be given when there are multiple states for destination')
            self.assertEqual(ErrorCode.NEXT_STATE_IS_REQUIRED, e.code)


        # There are STATE 4 and STATE 5 as next. State among STATE 4 and STATE 5 must be given to switch, not other state
        try:
            TransitionService.approve_transition(self.objects[0], self.field, self.user4, next_state=State.objects.get(label='s3'))
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e),
                             "Invalid state is given(%s). Valid states is(are) %s" % (
                                 State.objects.get(label='s3').__unicode__(), ','.join([ast.__unicode__() for ast in State.objects.filter(label__in=['s4', 's5'])])))
            self.assertEqual(ErrorCode.INVALID_NEXT_STATE_FOR_USER, e.code)




        # There are STATE 4 and STATE 5 as next. After one of them is given to approvement, the state must be switch to it immediately.
        self.assertEqual(State.objects.get(label='s3'), getattr(self.objects[0], self.field))

        TransitionService.approve_transition(self.objects[0], self.field, self.user4, next_state=State.objects.get(label='s5'))

        self.assertEqual(State.objects.get(label='s5'), getattr(self.objects[0], self.field))

        approvements = Approvement.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s3',
            meta__transition__destination_state__label='s5'
        )
        self.assertEqual(1, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertEqual(self.user4, approvements[0].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)
