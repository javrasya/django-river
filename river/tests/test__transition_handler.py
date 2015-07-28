from river.models import State
from river.services.object import ObjectService
from river.services.transition import TransitionService
from river.signals import TransitionHandler
from river.tests.services.approvement_service_based_test import ApprovementServiceBasedTest

__author__ = 'ahmetdal'


class TransitionHandlerTest(ApprovementServiceBasedTest):
    def test_register_for_all(self):
        self.test_args = None
        self.test_kwargs = None

        def test_handler(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        TransitionHandler.register(test_handler)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user1)

        self.assertEqual((), self.test_args)
        self.assertDictEqual(
            {
                'field': 'my_field',
                'object': self.objects[0],
                'source_state': State.objects.get(label='s1'),
                'destination_state': State.objects.get(label='s2')
            }, self.test_kwargs)


        # Approved but no transition
        TransitionService.approve_transition(self.objects[0], self.field, self.user2)

        self.assertEqual((), self.test_args)
        self.assertDictEqual(
            {
                'field': 'my_field',
                'object': self.objects[0],
                'source_state': State.objects.get(label='s1'),
                'destination_state': State.objects.get(label='s2')
            }, self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user3)

        self.assertEqual((), self.test_args)
        self.assertDictEqual(
            {
                'field': 'my_field',
                'object': self.objects[0],
                'source_state': State.objects.get(label='s2'),
                'destination_state': State.objects.get(label='s3')
            }, self.test_kwargs)

    def test_register_for_an_object(self):
        self.test_args = None
        self.test_kwargs = None

        def test_handler(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        TransitionHandler.register(test_handler, workflow_object=self.objects[1], field='my_field')

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionHandler.register(test_handler, workflow_object=self.objects[0], field='my_field')
        TransitionService.approve_transition(self.objects[0], self.field, self.user3)

        self.assertEqual((), self.test_args)
        self.assertDictEqual(
            {
                'field': 'my_field',
                'object': self.objects[0],
                'source_state': State.objects.get(label='s2'),
                'destination_state': State.objects.get(label='s3')
            }, self.test_kwargs)

    def test_register_for_a_transition(self):
        self.test_args = None
        self.test_kwargs = None

        def test_handler(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        TransitionHandler.register(test_handler, source_state=State.objects.get(label='s2'), destination_state=State.objects.get(label='s3'))

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user1)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user2)

        self.assertIsNone(self.test_args)
        self.assertIsNone(self.test_kwargs)

        TransitionService.approve_transition(self.objects[0], self.field, self.user3)

        self.assertEqual((), self.test_args)
        self.assertDictEqual(
            {
                'field': 'my_field',
                'object': self.objects[0],
                'source_state': State.objects.get(label='s2'),
                'destination_state': State.objects.get(label='s3')
            }, self.test_kwargs)
