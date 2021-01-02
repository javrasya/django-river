from django.contrib.contenttypes.models import ContentType
from django.db.models import ProtectedError
from django.test import TestCase
from hamcrest import assert_that, calling, raises
from river.models import APPROVED, TransitionApproval
from river.models.factories import StateObjectFactory, TransitionApprovalMetaFactory, TransitionMetaFactory, WorkflowFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory

# noinspection PyMethodMayBeStatic,DuplicatedCode
from rivertest.flowbuilder import FlowBuilder, RawState


class TransitionApprovalModelTest(TestCase):
    def test_shouldNotAllowWorkflowToBeDeletedWhenThereIsATransitionApproval(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = RawState("state_1")
        state2 = RawState("state_2")

        authorization_policies = []
        flow = FlowBuilder("my_field", content_type).with_transition(state1, state2, authorization_policies).build()

        assert_that(
            calling(flow.workflow.delete),
            raises(ProtectedError, "Cannot delete some instances of model 'Workflow' because they are referenced through .*")
        )

    def test_shouldNotAllowTheStateToBeDeletedWhenThereIsATransitionApprovalThatIsUsedAsSource(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = RawState("state_1")
        state2 = RawState("state_2")
        state3 = RawState("state_3")

        authorization_policies = []
        flow = (
            FlowBuilder("my_field", content_type)
            .with_transition(state1, state2, authorization_policies)
            .with_transition(state2, state3, authorization_policies)
            .build()
        )

        assert_that(
            calling(flow.get_state(state2).delete),
            raises(ProtectedError, "Cannot delete some instances of model 'State' because they are referenced through .*")
        )

    def test_shouldNotAllowTheStateToBeDeletedWhenThereIsATransitionApprovalThatIsUsedAsDestination(self):
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = RawState("state_1")
        state2 = RawState("state_2")
        state3 = RawState("state_3")

        authorization_policies = []
        flow = (
            FlowBuilder("my_field", content_type)
            .with_transition(state1, state2, authorization_policies)
            .with_transition(state2, state3, authorization_policies)
            .build()
        )

        assert_that(
            calling(flow.get_state(state3).delete),
            raises(ProtectedError, "Cannot delete some instances of model 'State' because they are referenced through .*")
        )
