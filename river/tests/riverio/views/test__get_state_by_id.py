from httplib import OK
import json

from django.conf import settings
from django.http.response import HttpResponseForbidden, HttpResponseNotFound
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from apps.riverio.views.serializers.state import StateSerializer

__author__ = 'ahmetdal'


class test_GetStateByIdView(APITestCase):
    def setUp(self):
        from apps.riverio.models.factories import StateObjectFactory

        super(test_GetStateByIdView, self).setUp()

        self.state = StateObjectFactory()
        self.application = self.state.application


    def test_get_state_by_id_view(self):
        result = self.client.get(reverse('state-detail', args=[self.state.pk]))
        self.assertEqual(HttpResponseForbidden.status_code, result.status_code)

        result = self.client.get(reverse('state-detail', args=[self.state.pk]), **{settings.TOKEN_KEY: 'test'})
        self.assertEqual(HttpResponseForbidden.status_code, result.status_code)

        result = self.client.get(reverse('state-detail', args=[self.state.pk + 1]), **{settings.TOKEN_KEY: self.application.applicationtoken.key})
        self.assertEqual(HttpResponseNotFound.status_code, result.status_code)
        content = json.loads(result.content)
        self.assertIn('detail', content)
        self.assertEqual("Not found", content['detail'])

        result = self.client.get(reverse('state-detail', args=[self.state.pk]), **{settings.TOKEN_KEY: self.application.applicationtoken.key})
        self.assertEqual(OK, result.status_code)

        content = json.loads(result.content)
        self.assertEqual(StateSerializer(self.state).data, content)

        self.assertNotIn('detail', content)
        self.assertIn('id', content)
        self.assertIn('label', content)
        self.assertIn('application', content)



