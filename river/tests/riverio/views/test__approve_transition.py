from httplib import OK
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest

from apps.riverio.models import Object, State, Approvement, APPROVED
from apps.riverio.services.object import ObjectService
from apps.riverio.views.serializers.transition_process_serializer import APPROVE
from tests.apps.riverio.views.approvement_service_based_view_test import ApprovementServiceBasedViewTest


__author__ = 'ahmetdal'


class test__ApproveTransitionView(ApprovementServiceBasedViewTest):
    def test_approve_transition(self):
        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)
        # ####################
        # STATE 1 - STATE 2
        # Only User1(2001) can approve and after his approve state must be changed to STATE 2
        # ###################

        # Approved by user has no required permission for this transition
        obj = Object.objects.get(object_id=self.objects[0].pk)

        result = self.client.post(reverse('process_transition'),
                                  {'process_type': APPROVE, 'content_type_id': self.content_type.pk, 'object_id': obj.object_id, 'field_id': self.field.pk, 'user_id': self.user2.user_id},
                                  **{settings.TOKEN_KEY: self.application.applicationtoken.key})

        self.assertEqual(HttpResponseBadRequest.status_code, result.status_code)
        content = json.loads(result.content)
        self.assertIn('detail', content)
        self.assertEqual('There is no available state for destination for the user.', content['detail'])

        # Approved by user has no required permission for this transition

        result = self.client.post(reverse('process_transition'),
                                  {'process_type': APPROVE, 'content_type_id': self.content_type.pk, 'object_id': obj.object_id, 'field_id': self.field.pk, 'user_id': self.user3.user_id},
                                  **{settings.TOKEN_KEY: self.application.applicationtoken.key})

        self.assertEqual(HttpResponseBadRequest.status_code, result.status_code)
        content = json.loads(result.content)
        self.assertIn('detail', content)
        self.assertEqual('There is no available state for destination for the user.', content['detail'])

        # Approved by user has no required permission for this transition
        result = self.client.post(reverse('process_transition'),
                                  {'process_type': APPROVE, 'content_type_id': self.content_type.pk, 'object_id': obj.object_id, 'field_id': self.field.pk, 'user_id': self.user4.user_id},
                                  **{settings.TOKEN_KEY: self.application.applicationtoken.key})

        self.assertEqual(HttpResponseBadRequest.status_code, result.status_code)
        content = json.loads(result.content)
        self.assertIn('detail', content)
        self.assertEqual('There is no available state for destination for the user.', content['detail'])

        # Approved by user has required permission for this transition
        self.assertEqual(State.objects.get(label='s1'), obj.state)

        result = self.client.post(reverse('process_transition'),
                                  {'process_type': APPROVE, 'content_type_id': self.content_type.pk, 'object_id': obj.object_id, 'field_id': self.field.pk, 'user_id': self.user1.user_id},
                                  **{settings.TOKEN_KEY: self.application.applicationtoken.key})

        self.assertEqual(OK, result.status_code)
        content = json.loads(result.content)
        self.assertNotIn('detail', content)
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

        result = self.client.post(reverse('process_transition'),
                                  {'process_type': APPROVE, 'content_type_id': self.content_type.pk, 'object_id': obj.object_id, 'field_id': self.field.pk, 'user_id': self.user1.user_id},
                                  **{settings.TOKEN_KEY: self.application.applicationtoken.key})

        self.assertEqual(HttpResponseBadRequest.status_code, result.status_code)
        content = json.loads(result.content)
        self.assertIn('detail', content)
        self.assertEqual('There is no available state for destination for the user.', content['detail'])
