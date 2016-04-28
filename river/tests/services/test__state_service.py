from river.models.state import State
from river.services.object import ObjectService
from river.services.state import StateService
from river.tests.base_test import BaseTestCase

__author__ = 'ahmetdal'


class test__StateService(BaseTestCase):
    def test_get_available_states(self):
        self.initialize_normal_scenario()

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

    def test_get_initial_state(self):
        self.initialize_normal_scenario()

        self.assertEqual(State.objects.get(label='s1'), StateService.get_initial_state(self.content_type, self.field))

    def test_get_final_states(self):
        self.initialize_normal_scenario()

        self.assertListEqual(list(State.objects.filter(label__in=['s4.1', 's4.2', 's5.1', 's5.2'])), list(StateService.get_final_states(self.content_type, self.field)))
