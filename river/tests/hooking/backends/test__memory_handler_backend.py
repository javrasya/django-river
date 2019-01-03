from river.config import app_config
from river.hooking.backends.loader import load_callback_backend
from river.hooking.transition import PostTransitionHooking
from river.tests.base_test import BaseTestCase
from river.tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


def test_handler(*args, **kwargs):
    pass


class MemoryHookingBackendTest(BaseTestCase):
    def setUp(self):
        super(MemoryHookingBackendTest, self).setUp()
        self.field_name = "my_field"
        self.initialize_standard_scenario()
        app_config.HOOKING_BACKEND_CLASS = 'river.hooking.backends.memory.MemoryHookingBackend'
        self.handler_backend = load_callback_backend()
        self.handler_backend.callbacks = {}

    def test_register(self):
        objects = TestModelObjectFactory.create_batch(2)

        self.assertFalse('%s.%s_object%s_field_name%s' % (
            PostTransitionHooking.__module__, PostTransitionHooking.__name__, objects[1].pk, self.field_name) in self.handler_backend.callbacks)
        self.handler_backend.register(PostTransitionHooking, test_handler, objects[1], self.field_name)
        self.assertTrue(
            '%s.%s_object%s_field_name%s' % (PostTransitionHooking.__module__, PostTransitionHooking.__name__, objects[1].pk, self.field_name) in self.handler_backend.callbacks)
        self.assertEqual(test_handler.__name__, list(self.handler_backend.callbacks.values())[0].__name__)

    def test_get_handlers(self):
        object = TestModelObjectFactory.create_batch(1)[0]

        self.handler_backend.register(PostTransitionHooking, test_handler, object, self.field_name)
        callbacks = self.handler_backend.get_callbacks(PostTransitionHooking, object, self.field_name)
        self.assertEqual(1, len(callbacks))

        self.assertEqual(test_handler.__name__, callbacks[0].__name__)
