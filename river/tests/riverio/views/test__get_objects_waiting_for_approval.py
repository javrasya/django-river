from httplib import OK
import json

from django.conf import settings
from rest_framework.reverse import reverse

from apps.riverio.models import Application
from apps.riverio.services.object import ObjectService
from tests.apps.riverio.views.approvement_service_based_view_test import ApprovementServiceBasedViewTest


__author__ = 'ahmetdal'


class test_GetObjectsWaitingForApprovalView(ApprovementServiceBasedViewTest):
    def test_get_objects_waiting_for_approval(self):
        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)

        result = self.client.get(reverse('objects_waiting_for_approval_list', args=[self.content_type.pk, self.field.pk, self.user1.user_id]),
                                 **{settings.TOKEN_KEY: self.application.applicationtoken.key})
        self.assertEqual(OK, result.status_code)
        content = json.loads(result.content)
        self.assertTrue(isinstance(content, list))
        self.assertEqual(2, len(content))
        self.assertEqual(self.objects[0].pk, content[0]['object_id'])
        self.assertEqual(self.objects[1].pk, content[1]['object_id'])


