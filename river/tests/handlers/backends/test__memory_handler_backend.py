from river.handlers.backends.loader import load_handler_backend
from river.handlers.transition import PostTransitionHandler
from river.services.config import RiverConfig
from river.services.object import ObjectService
from river.tests.services.approvement_service_based_test import ApprovementServiceBasedTest

__author__ = 'ahmetdal'


class test_MemoryHandlerBackend(ApprovementServiceBasedTest):
    def setUp(self):
        super(test_MemoryHandlerBackend, self).setUp()
        RiverConfig.HANDLER_BACKEND_CLASS = 'river.handlers.backends.memory.MemoryHandlerBackend'
        self.handler_backend = load_handler_backend()
        self.handler_backend.handlers = {}

        ObjectService.register_object(self.objects[0], self.field)

    def test_register(self):
        def test_handler(*args, **kwargs):
            pass

        self.assertFalse('%s.%s_object%sfield%s' % (PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk, 'my_field') in self.handler_backend.handlers)
        self.handler_backend.register(PostTransitionHandler, test_handler, self.objects[1], 'my_field')
        self.assertTrue('%s.%s_object%sfield%s' % (PostTransitionHandler.__module__, PostTransitionHandler.__name__, self.objects[1].pk, 'my_field') in self.handler_backend.handlers)
        self.assertTrue(test_handler.__name__, self.handler_backend.handlers.values()[0].__name__)

    def test_get_handlers(self):
        def test_handler(*args, **kwargs):
            pass

        self.handler_backend.register(PostTransitionHandler, test_handler, self.objects[1], 'my_field')
        handlers = self.handler_backend.get_handlers(PostTransitionHandler, self.objects[1], 'my_field')
        self.assertEqual(1, len(handlers))

        self.assertEqual(test_handler.__name__, handlers[0].__name__)
