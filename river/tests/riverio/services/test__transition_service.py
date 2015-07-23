from esefpy.common.django.middlewares import tls

from mock import MagicMock

from apps.riverio.models import State, Approvement, APPROVED

from apps.riverio.models import Object
from apps.riverio.services.object import ObjectService
from apps.riverio.services.transition import TransitionService
from tests.apps.riverio.services.approvement_service_based_test import ApprovementServiceBasedTest


__author__ = 'ahmetdal'


class test__TransitionService(ApprovementServiceBasedTest):
    def test_approve_transition(self):

        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)
        # ####################
        # STATE 1 - STATE 2
        # Only User1(2001) can approve and after his approve state must be changed to STATE 2
        # ###################

        # Approved by user has no required permission for this transition
        tls.get_user = MagicMock(return_value=self.application.owner)
        obj = Object.objects.get(object_id=self.objects[0].pk)

        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        obj = Object.objects.get(object_id=self.objects[0].pk)

        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)

        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        obj = Object.objects.get(object_id=self.objects[0].pk)

        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)

        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        obj = Object.objects.get(object_id=self.objects[0].pk)

        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)

        self.assertEqual(State.objects.get(label='s1'), obj.state)

        TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id)

        obj = Object.objects.get(object_id=self.objects[0].pk)
        self.assertEqual(State.objects.get(label='s2'), obj.state)

        approvements = Approvement.objects.filter(
            content_type=self.content_type,
            object_id=obj.object_id,
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
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # ####################
        # STATE 2 - STATE 3
        # User2(2002) is first approver and User3(2003) is second approver. This must be done with turn. After approvement is done, state is gonna be changed to STATE 3
        # ####################

        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Turn is User2(2002)s, not User3(2003)s. After User2(2002) approved, User3(2003) can approve.
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # Approved by two user has required permission for this transition to get next state (order is user2(2002),user3(2003)).
        obj = Object.objects.get(object_id=self.objects[0].pk)

        self.assertEqual(State.objects.get(label='s2'), obj.state)

        TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id)

        obj = Object.objects.get(object_id=self.objects[0].pk)
        self.assertEqual(State.objects.get(label='s2'), obj.state)

        approvements = Approvement.objects.filter(
            content_type=self.content_type,
            object_id=obj.object_id,
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
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        obj = Object.objects.get(object_id=self.objects[0].pk)

        self.assertEqual(State.objects.get(label='s2'), obj.state)

        TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id)

        obj = Object.objects.get(object_id=self.objects[0].pk)
        self.assertEqual(State.objects.get(label='s3'), obj.state)

        approvements = Approvement.objects.filter(
            content_type=self.content_type,
            object_id=obj.object_id,
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
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')



        # ####################
        # STATE 3 - STATE 4 or STATE 5
        # Only User4(2004) can approve by giving the exact next state and after his approve with his state must be changed to STATE 4 or STATE 5
        # ###################

        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # There are STATE 4 and STATE 5 as next. State must be given to switch
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'State must be given when there are multiple states for destination')


        # There are STATE 4 and STATE 5 as next. State among STATE 4 and STATE 5 must be given to switch, not other state
        obj = Object.objects.get(object_id=self.objects[0].pk)
        try:
            TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id, next_state_id=State.objects.get(label='s3').pk)
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message,
                             "Invalid state is given(%s). Valid states is(are) %s" % (
                                 State.objects.get(label='s3').__unicode__(), ','.join([ast.__unicode__() for ast in State.objects.filter(label__in=['s4', 's5'])])))




        # There are STATE 4 and STATE 5 as next. After one of them is given to approvement, the state must be switch to it immediately.
        obj = Object.objects.get(object_id=self.objects[0].pk)
        self.assertEqual(State.objects.get(label='s3'), obj.state)

        TransitionService.approve_transition(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id, next_state_id=State.objects.get(label='s5').pk)

        obj = Object.objects.get(object_id=self.objects[0].pk)
        self.assertEqual(State.objects.get(label='s5'), obj.state)

        approvements = Approvement.objects.filter(
            content_type=self.content_type,
            object_id=obj.object_id,
            field=self.field,
            status=APPROVED,
            meta__transition__source_state__label='s3',
            meta__transition__destination_state__label='s5'
        )
        self.assertEqual(1, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertEqual(self.user4, approvements[0].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)













