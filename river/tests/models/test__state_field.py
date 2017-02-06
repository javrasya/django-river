from copy import deepcopy

import mock
from django.db import models

from river.models.fields.state import StateField, _get_cls_identifier, class_field_rl
from river.tests.base_test import BaseTestCase
from river.tests.models.testmodel import TestModel
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

__author__ = 'ahmetdal'


class test_StateFIeld(BaseTestCase):
    def test_injections(self):
        self.assertTrue(hasattr(TestModel, 'proceedings'))
        self.assertTrue(hasattr(TestModel, 'proceeding'))
        self.assertTrue(hasattr(TestModel, 'is_workflow_completed'))
        self.assertTrue(hasattr(TestModel, 'proceed'))
        self.assertTrue(hasattr(TestModel, 'on_initial_state'))
        self.assertTrue(hasattr(TestModel, 'on_final_state'))
        self.assertTrue(hasattr(TestModel, 'get_initial_state'))
        self.assertTrue(hasattr(TestModel, 'get_available_proceedings'))
        self.assertTrue(hasattr(TestModel, 'initial_proceedings'))
        self.assertTrue(hasattr(TestModel, 'final_proceedings'))
        self.assertTrue(hasattr(TestModel, 'next_proceedings'))
        self.assertTrue(hasattr(TestModel, 'get_state'))
        self.assertTrue(hasattr(TestModel, 'set_state'))
        self.assertTrue(hasattr(TestModel, 'objects'))

    @mock.patch('django.db.models.fields.related.ForeignObject.contribute_to_class', mock.MagicMock())
    @mock.patch('river.models.fields.state.StateField._StateField__add_to_class', mock.MagicMock())
    def test_triggering_multiple_time(self):
        class TestModelForTriggeringMultipleTime(models.Model):
            pass

        field = StateField()
        class_field_rl_cp = deepcopy(class_field_rl)

        field.contribute_to_class(TestModelForTriggeringMultipleTime, 'status')

        class_field_rl_cp.update({_get_cls_identifier(TestModelForTriggeringMultipleTime): 'status'})
        self.assertDictEqual(class_field_rl_cp, class_field_rl)

        field.contribute_to_class(TestModelForTriggeringMultipleTime, 'status')

        self.assertDictEqual(class_field_rl_cp, class_field_rl)

        try:
            field.contribute_to_class(TestModelForTriggeringMultipleTime, 'status2')
            self.assertFalse(True, "River exception with error code %d, must have been raised")
        except RiverException as re:
            self.assertEqual(ErrorCode.MULTIPLE_STATE_FIELDS, re.code)
        else:
            self.assertFalse(True, "River exception with error code %d, must have been raised")
