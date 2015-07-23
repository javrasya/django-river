from django.contrib.auth.models import User
from esefpy.common.django.middlewares import tls
from mock import MagicMock

from apps.riverio.models import State
from apps.riverio.services.object import ObjectService
from apps.riverio.services.state import StateService
from tests.apps.riverio.services.approvement_service_based_test import ApprovementServiceBasedTest


__author__ = 'ahmetdal'


class test__StateService(ApprovementServiceBasedTest):
    def test_get_available_states(self):
        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)

        tls.get_user = MagicMock(return_value=self.application.owner)
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id, include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id)
        self.assertEqual(0, available_states.count())

        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id, include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id)
        self.assertEqual(0, available_states.count())

        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id, include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id)
        self.assertEqual(0, available_states.count())

        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id, include_user=True)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])

        available_states = StateService.get_available_states(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])





