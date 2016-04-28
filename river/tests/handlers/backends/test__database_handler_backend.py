from river.config import app_config
from river.handlers.backends.loader import load_handler_backend
from river.handlers.transition import PostTransitionHandler
from river.models.handler import Handler
from river.services.object import ObjectService
from river.tests.base_test import BaseTestCase

__author__ = 'ahmetdal'


def test_handler(*args, **kwargs):
    pass


class test_DatabaseHandlerBackend(BaseTestCase):
    def setUp(self):
        super(test_DatabaseHandlerBackend, self).setUp()
        self.initialize_normal_scenario()
        app_config.HANDLER_BACKEND_CLASS = 'river.handlers.backends.database.DatabaseHandlerBackend'
        self.handler_backend = load_handler_backend()
        self.handler_backend.handlers = {}

        ObjectService.register_object(self.objects[0], self.field)

    def test_register(self):
        self.assertEqual(0, Handler.objects.count())
        self.assertFalse('%s.%s_object%sfield%s' % (
            PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk,
            'my_field') in self.handler_backend.handlers)

        self.handler_backend.register(PostTransitionHandler, test_handler, self.objects[1], 'my_field')

        self.assertEqual(1, Handler.objects.filter(hash='%s.%s_object%sfield%s' % (
            PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk, 'my_field')).count())
        self.assertTrue('%s.%s_object%sfield%s' % (
            PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk,
            'my_field') in self.handler_backend.handlers)
        self.assertEqual(test_handler.__name__, list(self.handler_backend.handlers.values())[0].__name__)

    def test_register_in_multiprocessing(self):
        from multiprocessing import Process, Queue

        self.handler_backend.register(PostTransitionHandler, test_handler, self.objects[1], 'my_field')
        self.assertEqual(1, Handler.objects.count())

        def worker2(q):
            second_handler_backend = load_handler_backend()
            handlers = second_handler_backend.get_handlers(PostTransitionHandler, self.objects[1], 'my_field')
            q.put([f.__name__ for f in handlers])

        q = Queue()
        p2 = Process(target=worker2, args=(q,))

        p2.start()

        handlers = q.get(timeout=1)
        self.assertEqual(1, len(handlers))
        self.assertEqual(test_handler.__name__, handlers[0])

    def test_get_handlers(self):
        self.handler_backend.register(PostTransitionHandler, test_handler, self.objects[1], 'my_field')
        handlers = self.handler_backend.get_handlers(PostTransitionHandler, self.objects[1], 'my_field')
        self.assertEqual(1, len(handlers))

        self.assertEqual(test_handler.__name__, handlers[0].__name__)

    def test_get_handlers_in_multiprocessing(self):
        from multiprocessing import Process, Queue

        Handler.objects.update_or_create(
            hash='%s.%s_object%sfield%s' % (
                PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk, 'my_field'),
            defaults={
                'method': '%s.%s' % (test_handler.__module__, test_handler.__name__),
                'handler_cls': '%s.%s' % (PostTransitionHandler.__module__, PostTransitionHandler.__name__),
            }
        )

        def worker2(q):
            handlers = self.handler_backend.get_handlers(PostTransitionHandler, self.objects[1], 'my_field')
            q.put([f.__name__ for f in handlers])

        q = Queue()
        p2 = Process(target=worker2, args=(q,))

        p2.start()

        handlers = q.get(timeout=1)
        self.assertEqual(1, len(handlers))
        self.assertEqual(test_handler.__name__, handlers[0])
