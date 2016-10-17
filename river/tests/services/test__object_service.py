from river.models.proceeding import Proceeding
from river.services.object import ObjectService
from river.services.state import StateService
from river.tests.base_test import BaseTestCase
from river.tests.models.testmodel import TestModel, TestModelWithoutStateField
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


# noinspection PyPep8Naming
class test_ObjectService(BaseTestCase):
    def test_init(self):
        self.initialize_normal_scenario()

        ObjectService.register_object(self.objects[0])
        ObjectService.register_object(self.objects[1])

        initial_state = StateService.get_initial_state(self.content_type)

        self.assertEqual(initial_state, self.objects[0].get_state())
        self.assertEqual(18, Proceeding.objects.count())

    def test_get_objects_waiting_for_approval_for_user(self):
        self.initialize_normal_scenario()

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.user1)
        self.assertEqual(2, on_approval_objects.count())
        self.assertEqual(self.objects[0], on_approval_objects[0])

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.user2)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.user3)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type, self.user4)
        self.assertEqual(0, on_approval_objects.count())

    def test_get_field(self):
        field = ObjectService.get_field(TestModel)
        self.assertEqual('my_field', field.name)

        try:
            ObjectService.get_field(TestModelWithoutStateField)
            self.assertFalse(True, "Trying getting field from a model does not contains state field should have thrown the error with code '8'")
        except RiverException as re:
            self.assertEqual(ErrorCode.NO_STATE_FIELD, re.code)
