from httplib import OK

from django.conf import settings
from django.core.urlresolvers import reverse

from apps.riverio.models import Object, Approvement
from apps.riverio.services.state import StateService
from tests.apps.riverio.views.approvement_service_based_view_test import ApprovementServiceBasedViewTest

__author__ = 'ahmetdal'


class test_RegisterObjectView(ApprovementServiceBasedViewTest):
    def test_register_object(self):
        self.assertEqual(0, Approvement.objects.count())

        result = self.client.post(reverse('register_object'),
                                  {'content_type_id': self.content_type.pk, 'object_id': self.objects[0].pk, 'field_id': self.field.pk},
                                  **{settings.TOKEN_KEY: self.application.applicationtoken.key})

        obj = Object.objects.get(object_id=self.objects[0].pk)

        self.assertEqual(OK, result.status_code)
        initial_state = StateService.get_init_state(self.content_type.pk, self.field.pk)
        self.assertEqual(initial_state, obj.state)
        self.assertEqual(9, Approvement.objects.count())
