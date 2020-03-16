from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.test import TestCase
from hamcrest import assert_that, has_property, is_, instance_of

from river.core.classworkflowobject import ClassWorkflowObject
from river.core.instanceworkflowobject import InstanceWorkflowObject
from river.core.riverobject import RiverObject
from river.models import State
from river.models.factories import StateObjectFactory, TransitionApprovalMetaFactory, WorkflowFactory, TransitionMetaFactory
from river.tests.models import BasicTestModel


# noinspection PyMethodMayBeStatic
class StateFieldTest(TestCase):

    def test_shouldInjectTheField(self):  # pylint: disable=no-self-use
        assert_that(BasicTestModel, has_property('river', is_(instance_of(RiverObject))))
        assert_that(BasicTestModel.river, has_property('my_field', is_(instance_of(ClassWorkflowObject))))

        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory.create(label="state1")
        state2 = StateObjectFactory.create(label="state2")

        workflow = WorkflowFactory(content_type=content_type, field_name="my_field", initial_state=state1)

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
            priority=0
        )
        test_model = BasicTestModel.objects.create()
        assert_that(test_model, has_property('river', is_(instance_of(RiverObject))))
        assert_that(test_model.river, has_property('my_field', is_(instance_of(InstanceWorkflowObject))))
        assert_that(BasicTestModel.river.my_field, has_property('initial_state', is_(instance_of(State))))
        assert_that(BasicTestModel.river.my_field, has_property('final_states', is_(instance_of(QuerySet))))

        assert_that(test_model.river.my_field, has_property('approve', has_property("__call__")))
        assert_that(test_model.river.my_field, has_property('on_initial_state', is_(instance_of(bool))))
        assert_that(test_model.river.my_field, has_property('on_final_state', is_(instance_of(bool))))
