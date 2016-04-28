from river.models.state import State
from river.models.proceeding import Proceeding, APPROVED

from river.services.object import ObjectService
from river.services.transition import TransitionService
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException
from river.tests.base_test import BaseTestCase

__author__ = 'ahmetdal'


class test__TransitionService(BaseTestCase):
    def test_proceed(self):
        self.initialize_normal_scenario()

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)
        # ####################
        # STATE 1 - STATE 2
        # Only User1(2001) can proceed and after his proceed state must be changed to STATE 2
        # ###################

        # Proceeded by user has no required permission for this transition

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # Proceeded by user has no required permission for this transition

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # Proceeded by user has no required permission for this transition

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Proceeded by user has required permission for this transition

        self.assertEqual(State.objects.get(label='s1'), getattr(self.objects[0], self.field))

        TransitionService.proceed(self.objects[0], self.field, self.user1)

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))

        proceedings = Proceeding.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s1',
            meta__transition__destination_state__label='s2'
        )
        self.assertEqual(1, proceedings.count())
        self.assertIsNotNone(proceedings[0].transactioner)
        self.assertEqual(self.user1, proceedings[0].transactioner)
        self.assertIsNotNone(proceedings[0].transaction_date)

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # ####################
        # STATE 2 - STATE 3
        # User2(2002) is first proceeder and User3(2003) is second proceeder. This must be done with turn. After proceeding is done, state is gonna be changed to STATE 3
        # ####################

        # Proceeded by user has no required permission for this transition
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Proceeded by user has no required permission for this transition
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Turn is User2(2002)s, not User3(2003)s. After User2(2002) proceeded, User3(2003) can proceed.
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # Proceeded by two user has required permission for this transition to get next state (order is user2(2002),user3(2003)).

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))
        TransitionService.proceed(self.objects[0], self.field, self.user2)

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))

        proceedings = Proceeding.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s2',
            meta__transition__destination_state__label='s3'
        )
        self.assertEqual(1, proceedings.count())
        self.assertIsNotNone(proceedings[0].transactioner)
        self.assertEqual(self.user2, proceedings[0].transactioner)
        self.assertIsNotNone(proceedings[0].transaction_date)

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        self.assertEqual(State.objects.get(label='s2'), getattr(self.objects[0], self.field))

        TransitionService.proceed(self.objects[0], self.field, self.user3)

        self.assertEqual(State.objects.get(label='s3'), getattr(self.objects[0], self.field))

        proceedings = Proceeding.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s2',
            meta__transition__destination_state__label='s3'
        )
        self.assertEqual(2, proceedings.count())
        self.assertIsNotNone(proceedings[0].transactioner)
        self.assertIsNotNone(proceedings[1].transactioner)
        self.assertEqual(self.user2, proceedings[0].transactioner)
        self.assertEqual(self.user3, proceedings[1].transactioner)
        self.assertIsNotNone(proceedings[0].transaction_date)
        self.assertIsNotNone(proceedings[1].transaction_date)

        try:
            TransitionService.proceed(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)



        # ####################
        # STATE 3 - STATE 4 or STATE 5
        # Only User4(2004) can proceed by giving the exact next state and after his proceed with his state must be changed to STATE 4 or STATE 5
        # ###################

        # Proceeded by user has no required permission for this transition
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user1)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Proceeded by user has no required permission for this transition
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user2)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)

        # Proceeded by user has no required permission for this transition
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user3)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'There is no available state for destination for the user.')
            self.assertEqual(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, e.code)


        # There are STATE 4 and STATE 5 as next. State must be given to switch
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user4)
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e), 'State must be given when there are multiple states for destination')
            self.assertEqual(ErrorCode.NEXT_STATE_IS_REQUIRED, e.code)


        # There are STATE 4 and STATE 5 as next. State among STATE 4 and STATE 5 must be given to switch, not other state
        try:
            TransitionService.proceed(self.objects[0], self.field, self.user4, next_state=State.objects.get(label='s3'))
            self.fail('Exception was expected')
        except RiverException as e:
            self.assertEqual(str(e),
                             "Invalid state is given(%s). Valid states is(are) %s" % (
                                 State.objects.get(label='s3').__unicode__(), ','.join([ast.__unicode__() for ast in State.objects.filter(label__in=['s4', 's5'])])))
            self.assertEqual(ErrorCode.INVALID_NEXT_STATE_FOR_USER, e.code)




        # There are STATE 4 and STATE 5 as next. After one of them is given to proceeding, the state must be switch to it immediately.
        self.assertEqual(State.objects.get(label='s3'), getattr(self.objects[0], self.field))

        TransitionService.proceed(self.objects[0], self.field, self.user4, next_state=State.objects.get(label='s5'))

        self.assertEqual(State.objects.get(label='s5'), getattr(self.objects[0], self.field))

        proceedings = Proceeding.objects.filter(
            workflow_object=self.objects[0],
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s3',
            meta__transition__destination_state__label='s5'
        )
        self.assertEqual(1, proceedings.count())
        self.assertIsNotNone(proceedings[0].transactioner)
        self.assertEqual(self.user4, proceedings[0].transactioner)
        self.assertIsNotNone(proceedings[0].transaction_date)
