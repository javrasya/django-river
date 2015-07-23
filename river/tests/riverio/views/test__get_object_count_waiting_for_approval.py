from httplib import OK
import json

from django.conf import settings
from rest_framework.reverse import reverse

from apps.riverio.services.object import ObjectService
from tests.apps.riverio.views.approvement_service_based_view_test import ApprovementServiceBasedViewTest


__author__ = 'ahmetdal'


# noinspection PyPep8Naming
class test_GetObjectCountWaitingForApprovalView(ApprovementServiceBasedViewTest):
    def test_get_object_count_waiting_for_approval(self):
        ObjectService.register_object(self.content_type.pk, self.objects[0].pk, self.field.pk)
        ObjectService.register_object(self.content_type.pk, self.objects[1].pk, self.field.pk)

        result = self.client.get(reverse('object_count_waiting_for_approval', args=[self.content_type.pk, self.field.pk, self.user1.user_id]),
                                 **{settings.TOKEN_KEY: self.application.applicationtoken.key})
        self.assertEqual(OK, result.status_code)
        content = json.loads(result.content)
        self.assertIn('count', content)
        self.assertEqual(2, content['count'])


