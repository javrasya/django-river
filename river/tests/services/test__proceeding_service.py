from river.models import State, Proceeding
from river.services.proceeding import ProceedingService
from river.services.object import ObjectService
from river.tests.services.proceeding_service_based_test import ProceedingServiceBasedTest

__author__ = 'ahmetdal'


class test_ProceedingService(ProceedingServiceBasedTest):
    def test_get_proceedings_object_waiting_for_approval_without_skip(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field, [self.objects[0].my_field], user=self.user1)
        self.assertEqual(1, proceedings.count())

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field, [self.objects[0].my_field], user=self.user2)
        self.assertEqual(0, proceedings.count())

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field, [self.objects[0].my_field], user=self.user3)
        self.assertEqual(0, proceedings.count())

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field, [self.objects[0].my_field], user=self.user4)
        self.assertEqual(0, proceedings.count())

    def test_get_next_proceedings(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(9, proceedings.count())

        self.objects[0].proceed(self.user1)

        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(8, proceedings.count())

        self.objects[0].proceed(self.user2)


        # Two proceedings exist on same level
        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(8, proceedings.count())

        self.objects[0].proceed(self.user3)

        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(6, proceedings.count())

        self.objects[0].proceed(self.user4, next_state=State.objects.get(label='s4'))
        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(2, proceedings.count())

        self.objects[0].proceed(self.user4, next_state=State.objects.get(label='s4.1'))
        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(0, proceedings.count())

    def test_get_proceedings_object_waiting_for_approval_with_skip(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        proceedings = self.objects[1].get_available_proceedings(self.user1)
        self.assertEqual(1, proceedings.count())
        self.assertEqual(State.objects.get(label='s2'), proceedings[0].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s2')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field, [self.objects[1].my_field], user=self.user2)
        self.assertEqual(1, proceedings.count())
        self.assertEqual(State.objects.get(label='s3'), proceedings[0].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s3')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(2, proceedings.count())
        self.assertEqual(State.objects.get(label='s4'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), proceedings[1].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(3, proceedings.count())
        self.assertEqual(State.objects.get(label='s5'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.1'), proceedings[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), proceedings[2].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=False)
        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s5')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(3, proceedings.count())
        self.assertEqual(State.objects.get(label='s4'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), proceedings[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), proceedings[2].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4', 's5'])
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(4, proceedings.count())
        self.assertEqual(State.objects.get(label='s4.1'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), proceedings[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), proceedings[2].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), proceedings[3].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4.1', 's5.1'])
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(2, proceedings.count())
        self.assertEqual(State.objects.get(label='s4.2'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), proceedings[1].meta.transition.destination_state)
