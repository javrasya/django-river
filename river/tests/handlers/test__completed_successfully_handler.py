from river.handlers.completed_successfully import CompletedSuccessfullyHandler
from river.handlers.transition import TransitionHandler
from river.models import State, Transition
from river.services.object import ObjectService
from river.services.transition import TransitionService
from river.tests.services.approvement_service_based_test import ApprovementServiceBasedTest

__author__ = 'ahmetdal'


class test_CompletedSuccessfullyHandler(ApprovementServiceBasedTest):
    def setUp(self):
        super(test_CompletedSuccessfullyHandler, self).setUp()
        transition = Transition.objects.get(source_state__label='s2', destination_state__label='s3')
        Transition.objects.filter(pk__gt=transition.pk).delete()

    def test_register_for_all(self):
        self.test_args = None
        self.test_kwargs = None

        def test_handler(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        CompletedSuccessfullyHandler.register(test_handler)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        # Approved but no transition
        TransitionService.approve_transition(self.objects[0], self.field, self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user3)

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

        CompletedSuccessfullyHandler.register(test_handler, self.objects[0], 'my_field')

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        # Approved but no transition
        TransitionService.approve_transition(self.objects[0], self.field, self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user3)

        self.assertEqual((), self.test_args)
        self.assertDictEqual(
            {
                'field': 'my_field',
                'object': self.objects[0]
            }, self.test_kwargs)
