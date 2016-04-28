from unittest import skip

from river.handlers.completed import PostCompletedHandler
from river.models.transition import Transition
from river.services.object import ObjectService
from river.services.transition import TransitionService
from river.tests.base_test import BaseTestCase

__author__ = 'ahmetdal'


class test_CompletedHandler(BaseTestCase):
    def setUp(self):
        super(test_CompletedHandler, self).setUp()
        self.initialize_normal_scenario()
        transition = Transition.objects.get(source_state__label='s2', destination_state__label='s3')
        Transition.objects.filter(pk__gt=transition.pk).delete()

    @skip("workflow object is now required to register")
    def test_register_for_all(self):
        self.initialize_normal_scenario()
        self.test_args = None
        self.test_kwargs = None

        def test_handler(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        PostCompletedHandler.register(test_handler)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.proceed(self.objects[0], self.field, self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        # Proceeded but no transition
        TransitionService.proceed(self.objects[0], self.field, self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.proceed(self.objects[0], self.field, self.user3)

        self.assertEqual((), self.test_args)
        self.assertDictEqual(
            {
                'field': 'my_field',
                'object': self.objects[0]
            }, self.test_kwargs)

    def test_register_for_an_object(self):

        self.test_args = None
        self.test_kwargs = None

        def test_handler(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        PostCompletedHandler.register(test_handler, self.objects[0], 'my_field')

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.proceed(self.objects[0], self.field, self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        # Proceeded but no transition
        TransitionService.proceed(self.objects[0], self.field, self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.proceed(self.objects[0], self.field, self.user3)

        self.assertEqual((self.objects[0], 'my_field'), self.test_args)
