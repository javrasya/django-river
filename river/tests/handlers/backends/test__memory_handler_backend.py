from river.config import app_config
from river.handlers.backends.loader import load_handler_backend
from river.handlers.transition import PostTransitionHandler
from river.services.object import ObjectService
from river.tests.base_test import BaseTestCase

__author__ = 'ahmetdal'


def test_handler(*args, **kwargs):
    pass


class test_MemoryHandlerBackend(BaseTestCase):
    def setUp(self):
        super(test_MemoryHandlerBackend, self).setUp()
        self.initialize_normal_scenario()
        app_config.HANDLER_BACKEND_CLASS = 'river.handlers.backends.memory.MemoryHandlerBackend'
        self.handler_backend = load_handler_backend()
        self.handler_backend.handlers = {}

        ObjectService.register_object(self.objects[0], self.field)

    def test_register(self):
        self.assertFalse('%s.%s_object%sfield%s' % (
            PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk,
            'my_field') in self.handler_backend.handlers)
        self.handler_backend.register(PostTransitionHandler, test_handler, self.objects[1], 'my_field')
        self.assertTrue('%s.%s_object%sfield%s' % (
            PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk,
            'my_field') in self.handler_backend.handlers)
        self.assertEqual(test_handler.__name__, list(self.handler_backend.handlers.values())[0].__name__)

    def test_get_handlers(self):
        self.handler_backend.register(PostTransitionHandler, test_handler, self.objects[1], 'my_field')
        handlers = self.handler_backend.get_handlers(PostTransitionHandler, self.objects[1], 'my_field')
        self.assertEqual(1, len(handlers))

        self.assertEqual(test_handler.__name__, handlers[0].__name__)
