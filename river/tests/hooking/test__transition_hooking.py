from django.contrib.auth.models import Permission

from river.models import TransitionApproval
from river.tests.base_test import BaseTestCase
from river.tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


class TransitionHooking(BaseTestCase):

    def test_register_for_an_object(self):
        self.initialize_standard_scenario()
        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        objects = TestModelObjectFactory.create_batch(2)

        objects[1].river.my_field.hook_post_transition(test_callback)

        objects[0].river.my_field.approve(as_user=self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.hook_post_transition(test_callback)

        objects[0].river.my_field.approve(as_user=self.user3)

        self.assertEqual((objects[0], "my_field"), self.test_args)

        self.assertDictEqual(
            {
                'transition_approval': TransitionApproval.objects.get(object_id=objects[0].pk, source_state=self.state2, destination_state=self.state3,
                                                                      permissions__in=Permission.objects.filter(user=self.user3))
            }, self.test_kwargs)

    def test_register_for_a_transition(self):
        self.initialize_standard_scenario()

        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        objects = TestModelObjectFactory.create_batch(2)
        objects[0].river.my_field.hook_post_transition(test_callback, source_state=self.state2, destination_state=self.state3)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user3)

        self.assertEqual((objects[0], "my_field"), self.test_args)
        self.assertDictEqual(
            {
                'transition_approval': TransitionApproval.objects.get(object_id=objects[0].pk, source_state=self.state2, destination_state=self.state3,
                                                                      permissions__in=Permission.objects.filter(user=self.user3))
            }, self.test_kwargs)
