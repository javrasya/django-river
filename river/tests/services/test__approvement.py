from river.models import State, Approvement
from river.services.approvement import ApprovementService
from river.services.object import ObjectService
from river.tests.services.approvement_service_based_test import ApprovementServiceBasedTest

__author__ = 'ahmetdal'


class test_ApprovementService(ApprovementServiceBasedTest):
    def test_get_approvements_object_waiting_for_approval_without_skip(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, [self.objects[0].my_field], user=self.user1)
        self.assertEqual(1, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, [self.objects[0].my_field], user=self.user2)
        self.assertEqual(0, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, [self.objects[0].my_field], user=self.user3)
        self.assertEqual(0, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, [self.objects[0].my_field], user=self.user4)
        self.assertEqual(0, approvements.count())

    def test_get_next_approvements(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        approvements = ApprovementService.get_next_approvements(self.objects[0], self.field)
        self.assertEqual(9, approvements.count())

        self.objects[0].approve(self.user1)

        approvements = ApprovementService.get_next_approvements(self.objects[0], self.field)
        self.assertEqual(8, approvements.count())

        self.objects[0].approve(self.user2)


        # Two approvements exist on same level
        approvements = ApprovementService.get_next_approvements(self.objects[0], self.field)
        self.assertEqual(8, approvements.count())

        self.objects[0].approve(self.user3)

        approvements = ApprovementService.get_next_approvements(self.objects[0], self.field)
        self.assertEqual(6, approvements.count())

        self.objects[0].approve(self.user4, next_state=State.objects.get(label='s4'))
        approvements = ApprovementService.get_next_approvements(self.objects[0], self.field)
        self.assertEqual(2, approvements.count())

        self.objects[0].approve(self.user4, next_state=State.objects.get(label='s4.1'))
        approvements = ApprovementService.get_next_approvements(self.objects[0], self.field)
        self.assertEqual(0, approvements.count())

    def test_get_approvements_object_waiting_for_approval_with_skip(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        approvements = self.objects[1].get_available_approvements(self.user1)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s2'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s2')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, [self.objects[1].my_field], user=self.user2)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s3'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s3')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), approvements[1].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(3, approvements.count())
        self.assertEqual(State.objects.get(label='s5'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.1'), approvements[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), approvements[2].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=False)
        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s5')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(3, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), approvements[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[2].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4', 's5'])
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(4, approvements.count())
        self.assertEqual(State.objects.get(label='s4.1'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), approvements[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), approvements[2].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[3].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4.1', 's5.1'])
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, [self.objects[1].my_field], user=self.user4)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4.2'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[1].meta.transition.destination_state)
