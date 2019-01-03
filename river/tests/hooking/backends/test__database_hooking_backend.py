from river.config import app_config
from river.hooking.backends.loader import load_callback_backend
from river.hooking.transition import PostTransitionHooking
from river.models.callback import Callback
from river.tests.base_test import BaseTestCase
from river.tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


def test_callback(*args, **kwargs):
    pass


class DatabaseHookingBackendTest(BaseTestCase):
    def setUp(self):
        super(DatabaseHookingBackendTest, self).setUp()
        self.field_name = "my_field"
        self.initialize_standard_scenario()
        app_config.HOOKING_BACKEND_CLASS = 'river.hooking.backends.database.DatabaseHookingBackend'
        self.handler_backend = load_callback_backend()
        self.handler_backend.callbacks = {}

    def test_register(self):
        objects = TestModelObjectFactory.create_batch(2)

        self.assertEqual(0, Callback.objects.count())
        self.assertFalse('%s.%s_object%sfield%s' % (
            PostTransitionHooking.__module__, PostTransitionHooking.__name__, objects[1].pk,
            'my_field') in self.handler_backend.callbacks)

        self.handler_backend.register(PostTransitionHooking, test_callback, objects[1], self.field_name)

        self.assertEqual(1, Callback.objects.filter(hash='%s.%s_object%s_field_name%s' % (
            PostTransitionHooking.__module__, PostTransitionHooking.__name__, objects[1].pk, self.field_name)).count())
        self.assertTrue('%s.%s_object%s_field_name%s' % (
            PostTransitionHooking.__module__, PostTransitionHooking.__name__, objects[1].pk, self.field_name) in self.handler_backend.callbacks)
        self.assertEqual(test_callback.__name__, list(self.handler_backend.callbacks.values())[0].__name__)

    def test_register_in_multiprocessing(self):
        objects = TestModelObjectFactory.create_batch(2)

        from multiprocessing import Process, Queue

        self.handler_backend.register(PostTransitionHooking, test_callback, objects[1], self.field_name)
        self.assertEqual(1, Callback.objects.count())

        def worker2(q):
            second_handler_backend = load_callback_backend()
            handlers = second_handler_backend.get_callbacks(PostTransitionHooking, objects[1], self.field_name)
            q.put([f.__name__ for f in handlers])

        q = Queue()
        p2 = Process(target=worker2, args=(q,))

        p2.start()

        handlers = q.get(timeout=1)
        self.assertEqual(1, len(handlers))
        self.assertEqual(test_callback.__name__, handlers[0])

    def test_get_callbacks(self):
        objects = TestModelObjectFactory.create_batch(2)

        self.handler_backend.register(PostTransitionHooking, test_callback, objects[1], self.field_name)
        handlers = self.handler_backend.get_callbacks(PostTransitionHooking, objects[1], self.field_name)
        self.assertEqual(1, len(handlers))

        self.assertEqual(test_callback.__name__, handlers[0].__name__)

    def test_get_handlers_in_multiprocessing(self):
        objects = TestModelObjectFactory.create_batch(2)

        from multiprocessing import Process, Queue

        Callback.objects.update_or_create(
            hash='%s.%s_object%s_field_name%s' % (PostTransitionHooking.__module__, PostTransitionHooking.__name__, objects[1].pk, self.field_name),
            defaults={
                'method': '%s.%s' % (test_callback.__module__, test_callback.__name__),
                'hooking_cls': '%s.%s' % (PostTransitionHooking.__module__, PostTransitionHooking.__name__),
            }
        )

        def worker2(q):
            handlers = self.handler_backend.get_callbacks(PostTransitionHooking, objects[1], self.field_name)
            q.put([f.__name__ for f in handlers])

        q = Queue()
        p2 = Process(target=worker2, args=(q,))

        p2.start()

        handlers = q.get(timeout=1)
        self.assertEqual(1, len(handlers))
        self.assertEqual(test_callback.__name__, handlers[0])
