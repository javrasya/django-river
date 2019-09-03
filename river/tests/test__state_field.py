from django.contrib.contenttypes.models import ContentType

from river.models.factories import StateObjectFactory, TransitionApprovalMetaFactory, WorkflowFactory
from river.core.riverobject import RiverObject
from river.core.instanceworkflowobject import InstanceWorkflowObject
from river.core.classworkflowobject import ClassWorkflowObject
from river.tests.base_test import BaseTestCase
from river.tests.models import BasicTestModel

__author__ = 'ahmetdal'


class StateFieldTest(BaseTestCase):

    def test_injections(self):
        self.assertTrue(hasattr(BasicTestModel, 'river'))
        self.assertIsInstance(BasicTestModel.river, RiverObject)
        self.assertTrue(hasattr(BasicTestModel.river, "my_field"))
        self.assertIsInstance(BasicTestModel.river.my_field, ClassWorkflowObject)

        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory.create(label="state1")
        state2 = StateObjectFactory.create(label="state2")

        workflow = WorkflowFactory(content_type=content_type, field_name="my_field", initial_state=state1)

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0
        )
        test_model = BasicTestModel.objects.create()
        self.assertTrue(hasattr(test_model, "river"))
        self.assertIsInstance(test_model.river, RiverObject)
        self.assertTrue(hasattr(test_model.river, "my_field"))
        self.assertIsInstance(test_model.river.my_field, InstanceWorkflowObject)

        self.assertTrue(hasattr(test_model.river.my_field, "approve"))
        self.assertTrue(callable(test_model.river.my_field.approve))

        self.assertTrue(test_model.river.my_field.on_initial_state)
        self.assertFalse(test_model.river.my_field.on_final_state)

        self.assertEqual(state1, BasicTestModel.river.my_field.initial_state)
        self.assertEqual(1, BasicTestModel.river.my_field.final_states.count())
        self.assertEqual(state2, BasicTestModel.river.my_field.final_states[0])
