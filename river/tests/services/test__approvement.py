from river.models import State, Approvement
from river.services.approvement import ApprovementService
from river.services.object import ObjectService
from river.tests.services.approvement_service_based_test import ApprovementServiceBasedTest

__author__ = 'ahmetdal'


class test_ApprovementService(ApprovementServiceBasedTest):
    def test_get_approvements_object_waiting_for_approval_without_skip(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, self.user1, [self.objects[0].my_field], include_user=True)
        self.assertEqual(1, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, self.user2, [self.objects[0].my_field], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, self.user2, [self.objects[0].my_field], include_user=True)
        self.assertEqual(0, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, self.user3, [self.objects[0].my_field], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, self.user3, [self.objects[0].my_field], include_user=True)
        self.assertEqual(0, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, self.user4, [self.objects[0].my_field], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[0], self.field, self.user4, [self.objects[0].my_field], include_user=True)
        self.assertEqual(0, approvements.count())

    def test_get_approvements_object_waiting_for_approval_with_skip(self):
        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s2'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s2'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s2')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s3'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s3'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s3')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=False)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), approvements[1].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=True)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), approvements[1].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s5'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s5'), approvements[0].meta.transition.destination_state)

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

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4', 's5'])
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=False)
        self.assertEqual(4, approvements.count())
        self.assertEqual(State.objects.get(label='s4.1'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), approvements[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), approvements[2].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[3].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=True)
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

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=False)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4.2'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[1].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.objects[1], self.field, self.user1, [self.objects[1].my_field], include_user=True)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4.2'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[1].meta.transition.destination_state)
