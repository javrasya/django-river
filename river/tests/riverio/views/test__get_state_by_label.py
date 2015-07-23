from httplib import OK
import json

from django.conf import settings
from django.http.response import HttpResponseForbidden
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from apps.riverio.views.serializers.state import StateSerializer

__author__ = 'ahmetdal'


class test_GetStateByLabelView(APITestCase):
    def setUp(self):
        from apps.riverio.models.factories import StateObjectFactory

        super(test_GetStateByLabelView, self).setUp()

        self.state = StateObjectFactory()
        self.application = self.state.application


    def test_get_state_by_label_view(self):
        result = self.client.get("%s?label=%s" % (reverse('state-list'), self.state.label))
        self.assertEqual(HttpResponseForbidden.status_code, result.status_code)

        result = self.client.get('%s?label=%s' % (reverse('state-list'), self.state.label), **{settings.TOKEN_KEY: 'test'})
        self.assertEqual(HttpResponseForbidden.status_code, result.status_code)

        result = self.client.get('%s?label=%s' % (reverse('state-list'), 's2'), **{settings.TOKEN_KEY: self.application.applicationtoken.key})
        self.assertEqual(OK, result.status_code)
        content = json.loads(result.content)
        self.assertTrue(isinstance(content, list))
        self.assertEqual(0, len(content))

        result = self.client.get('%s?label=%s' % (reverse('state-list'), self.state.label), **{settings.TOKEN_KEY: self.application.applicationtoken.key})
        self.assertEqual(OK, result.status_code)

        content = json.loads(result.content)

        self.assertEqual([StateSerializer(self.state).data], content)
        state = content[0]
        self.assertNotIn('detail', state)
        self.assertIn('id', state)
        self.assertIn('label', state)
        self.assertIn('application', state)


