from river.models import Proceeding
from river.services.object import ObjectService
from river.services.state import StateService
from river.tests.services.proceeding_service_based_test import ProceedingServiceBasedTest

__author__ = 'ahmetdal'


# noinspection PyPep8Naming
class test_ObjectService(ProceedingServiceBasedTest):
    def test_init(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        initial_state = StateService.get_initial_state(self.content_type, self.field)

        self.assertEqual(initial_state, getattr(self.objects[0], self.field))
        self.assertEqual(18, Proceeding.objects.count())

    def test_get_objects_waiting_for_approval_for_user(self):
        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.field, self.user1)
        self.assertEqual(0, on_approval_objects.count())

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)
        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.field, self.user1)
        self.assertEqual(2, on_approval_objects.count())
        self.assertEqual(self.objects[0], on_approval_objects[0])

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.field, self.user2)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.field, self.user3)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.field, self.user4)
        self.assertEqual(0, on_approval_objects.count())
