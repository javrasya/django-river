from river.hooking.completed import PostCompletedHooking
from river.tests.base_test import BaseTestCase
from river.tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


class CompletedHookingTest(BaseTestCase):
    def setUp(self):
        super(CompletedHookingTest, self).setUp()
        self.initialize_standard_scenario()

    def test_register_for_an_object(self):
        objects = TestModelObjectFactory.create_batch(2)

        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        objects[0].river.my_field.hook_post_complete(test_callback)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        # Proceeded but no transition
        objects[0].river.my_field.approve(as_user=self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user3)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user4, next_state=self.state4)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        objects[0].river.my_field.approve(as_user=self.user4, next_state=self.state41)

        self.assertEqual((objects[0], "my_field"), self.test_args)
