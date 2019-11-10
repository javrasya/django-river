from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, has_length, has_item, has_property, none

from river.models import TransitionApproval, APPROVED, PENDING
from river.models.factories import WorkflowFactory, StateObjectFactory, TransitionApprovalMetaFactory, TransitionMetaFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory


# noinspection PyMethodMayBeStatic
class TransitionApprovalMetaModelTest(TestCase):

    def test_shouldNotDeleteApprovedTransitionWhenDeleted(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        meta1 = TransitionApprovalMetaFactory.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        BasicTestModelObjectFactory()
        TransitionApproval.objects.filter(workflow=workflow).update(status=APPROVED)
        approvals = TransitionApproval.objects.filter(workflow=workflow)
        assert_that(approvals, has_length(1))
        assert_that(approvals, has_item(has_property("meta", meta1)))

        meta1.delete()

        approvals = TransitionApproval.objects.filter(workflow=workflow)
        assert_that(approvals, has_length(1))
        assert_that(approvals, has_item(has_property("meta", none())))

    def test_shouldNotDeletePendingTransitionWhenDeleted(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        meta1 = TransitionApprovalMetaFactory.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        BasicTestModelObjectFactory()
        TransitionApproval.objects.filter(workflow=workflow).update(status=PENDING)
        assert_that(TransitionApproval.objects.filter(workflow=workflow), has_length(1))

        meta1.delete()

        assert_that(TransitionApproval.objects.filter(workflow=workflow), has_length(0))
