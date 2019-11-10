from django.contrib.contenttypes.models import ContentType
from django.db.models import ProtectedError
from django.test import TestCase
from hamcrest import assert_that, has_length, calling, raises

from river.models import TransitionApproval, APPROVED
from river.models.factories import WorkflowFactory, StateObjectFactory, TransitionApprovalMetaFactory, TransitionMetaFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory


# noinspection PyMethodMayBeStatic,DuplicatedCode
class TransitionApprovalModelTest(TestCase):

    def test_shouldNotAllowWorkflowToBeDeletedWhenThereIsATransitionApproval(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        TransitionApprovalMetaFactory.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        BasicTestModelObjectFactory()
        TransitionApproval.objects.filter(workflow=workflow).update(status=APPROVED)
        approvals = TransitionApproval.objects.filter(workflow=workflow)
        assert_that(approvals, has_length(1))

        assert_that(
            calling(workflow.delete),
            raises(ProtectedError, "Cannot delete some instances of model 'Workflow' because they are referenced through a protected foreign key")
        )

    def test_shouldNotAllowTheStateToBeDeletedWhenThereIsATransitionApprovalThatIsUsedAsSource(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state2,
            destination_state=state3,
        )

        TransitionApprovalMetaFactory.create(workflow=workflow, transition_meta=transition_meta_1, priority=0)
        TransitionApprovalMetaFactory.create(workflow=workflow, transition_meta=transition_meta_2, priority=0)

        BasicTestModelObjectFactory()
        TransitionApproval.objects.filter(workflow=workflow).update(status=APPROVED)
        approvals = TransitionApproval.objects.filter(workflow=workflow)
        assert_that(approvals, has_length(2))

        assert_that(
            calling(state2.delete),
            raises(ProtectedError, "Cannot delete some instances of model 'State' because they are referenced through a protected foreign key")
        )

    def test_shouldNotAllowTheStateToBeDeletedWhenThereIsATransitionApprovalThatIsUsedAsDestination(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state2,
            destination_state=state3,
        )

        TransitionApprovalMetaFactory.create(workflow=workflow, transition_meta=transition_meta_1, priority=0)
        TransitionApprovalMetaFactory.create(workflow=workflow, transition_meta=transition_meta_2, priority=0)

        BasicTestModelObjectFactory()
        TransitionApproval.objects.filter(workflow=workflow).update(status=APPROVED)
        approvals = TransitionApproval.objects.filter(workflow=workflow)
        assert_that(approvals, has_length(2))

        assert_that(
            calling(state3.delete),
            raises(ProtectedError, "Cannot delete some instances of model 'State' because they are referenced through a protected foreign key")
        )
