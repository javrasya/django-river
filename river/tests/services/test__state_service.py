from django.contrib.auth.models import User
from mock import MagicMock

from river.models import State
from river.services.object import ObjectService
from river.services.state import StateService
from river.tests.services.approvement_service_based_test import ApprovementServiceBasedTest

__author__ = 'ahmetdal'


class test__StateService(ApprovementServiceBasedTest):
    def test_get_available_states(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        available_states = StateService.get_available_states(self.objects[0], self.field, self.user2, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.objects[0], self.field, self.user2, include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(self.objects[0], self.field, self.user2)
        self.assertEqual(0, available_states.count())

        available_states = StateService.get_available_states(self.objects[0], self.field, self.user3, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.objects[0], self.field, self.user3, include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(self.objects[0], self.field, self.user3)
        self.assertEqual(0, available_states.count())

        available_states = StateService.get_available_states(self.objects[0], self.field, self.user4, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.objects[0], self.field, self.user4, include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(self.objects[0], self.field, self.user4)
        self.assertEqual(0, available_states.count())

        available_states = StateService.get_available_states(self.objects[0], self.field, self.user1, include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(self.objects[0], self.field, self.user1, include_user=True)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])

        available_states = StateService.get_available_states(self.objects[0], self.field, self.user1)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
