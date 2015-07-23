from esefpy.common.django.middlewares import tls
from mock import MagicMock

from apps.riverio.models import State, Approvement, Object
from apps.riverio.services.approvement import ApprovementService
from apps.riverio.services.object import ObjectService
from tests.apps.riverio.services.approvement_service_based_test import ApprovementServiceBasedTest


__author__ = 'ahmetdal'


class test_ApprovementService(ApprovementServiceBasedTest):



    def test_get_approvements_object_waiting_for_approval_without_skip(self):
        tls.get_user = MagicMock(return_value=self.application.owner)

        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[0].pk).state],
                                                                                       include_user=True)
        self.assertEqual(1, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[0].pk).state], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user2.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[0].pk).state], include_user=True)
        self.assertEqual(0, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[0].pk).state], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user3.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[0].pk).state], include_user=True)
        self.assertEqual(0, approvements.count())

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[0].pk).state], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[0].pk, self.field.pk, self.user4.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[0].pk).state], include_user=True)
        self.assertEqual(0, approvements.count())

    def test_get_approvements_object_waiting_for_approval_with_skip(self):
        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)

        tls.get_user = MagicMock(return_value=self.application.owner)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s2'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s2'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            content_type=self.content_type,
            field=self.field,
            object_id=self.objects[1].pk,
            meta__transition__destination_state=State.objects.get(label='s2')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s3'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s3'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            content_type=self.content_type,
            field=self.field,
            object_id=self.objects[1].pk,
            meta__transition__destination_state=State.objects.get(label='s3')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=False)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), approvements[1].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=True)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), approvements[1].meta.transition.destination_state)

        Approvement.objects.filter(
            content_type=self.content_type,
            field=self.field,
            object_id=self.objects[1].pk,
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s5'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s5'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            content_type=self.content_type,
            field=self.field,
            object_id=self.objects[1].pk,
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=False)
        Approvement.objects.filter(
            content_type=self.content_type,
            field=self.field,
            object_id=self.objects[1].pk,
            meta__transition__destination_state=State.objects.get(label='s5')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].meta.transition.destination_state)

        Approvement.objects.filter(
            content_type=self.content_type,
            field=self.field,
            object_id=self.objects[1].pk,
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4', 's5'])
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=False)
        self.assertEqual(4, approvements.count())
        self.assertEqual(State.objects.get(label='s4.1'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), approvements[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), approvements[2].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[3].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=True)
        self.assertEqual(4, approvements.count())
        self.assertEqual(State.objects.get(label='s4.1'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), approvements[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), approvements[2].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[3].meta.transition.destination_state)

        Approvement.objects.filter(
            content_type=self.content_type,
            field=self.field,
            object_id=self.objects[1].pk,
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4.1', 's5.1'])
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=False)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4.2'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[1].meta.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(self.content_type.pk, self.objects[1].pk, self.field.pk, self.user1.user_id,
                                                                                       [Object.objects.get(object_id=self.objects[1].pk).state], include_user=True)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4.2'), approvements[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[1].meta.transition.destination_state)












