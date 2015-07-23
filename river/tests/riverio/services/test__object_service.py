from esefpy.common.django.middlewares import tls
from mock import MagicMock

from apps.riverio.models import Object, Approvement
from apps.riverio.services.object import ObjectService
from apps.riverio.services.state import StateService
from tests.apps.riverio.services.approvement_service_based_test import ApprovementServiceBasedTest


__author__ = 'ahmetdal'


# noinspection PyPep8Naming
class test_ObjectService(ApprovementServiceBasedTest):
    def test_init(self):
        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)

        obj = Object.objects.get(object_id=self.objects[0].pk)

        initial_state = StateService.get_init_state(self.content_type.pk, self.field.pk)

        self.assertEqual(initial_state, obj.state)
        self.assertEqual(18, Approvement.objects.count())

    def test_get_objects_waiting_for_approval_for_user(self):
        tls.get_user = MagicMock(return_value=self.application.owner)
        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type.pk, self.field.pk, self.user1.user_id)
        self.assertEqual(0, on_approval_objects.count())

        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type.pk, self.field.pk, self.user1.user_id)
        self.assertEqual(2, on_approval_objects.count())
        self.assertEqual(self.objects[0].pk, on_approval_objects[0].object_id)

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type.pk, self.field.pk, self.user2.user_id)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type.pk, self.field.pk, self.user3.user_id)
        self.assertEqual(0, on_approval_objects.count())

        on_approval_objects = ObjectService.get_objects_waiting_for_approval(self.content_type.pk, self.field.pk, self.user4.user_id)
        self.assertEqual(0, on_approval_objects.count())











