from river.tests.base_test import BaseTestCase
from river.tests.models.testmodel import TestModel

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
