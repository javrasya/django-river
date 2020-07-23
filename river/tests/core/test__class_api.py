from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, equal_to, has_item, all_of, has_property, less_than, has_items, has_length

from river.models.factories import PermissionObjectFactory, UserObjectFactory, StateObjectFactory, GroupObjectFactory
from river.tests.models import BasicTestModel
# noinspection PyMethodMayBeStatic,DuplicatedCode
from rivertest.flowbuilder import RawState, AuthorizationPolicyBuilder, FlowBuilder


class ClassApiTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(ClassApiTest, self).__init__(*args, **kwargs)
        self.content_type = ContentType.objects.get_for_model(BasicTestModel)

    def test_shouldReturnNoApprovalWhenUserIsUnAuthorized(self):
        unauthorized_user = UserObjectFactory()
        authorized_permission = PermissionObjectFactory()

        state1 = RawState("state1")
        state2 = RawState("state2")

        authorization_policies = [AuthorizationPolicyBuilder().with_permission(authorized_permission).build()]
        FlowBuilder("my_field", self.content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .build()

        available_approvals = BasicTestModel.river.my_field.get_available_approvals(as_user=unauthorized_user)
        assert_that(available_approvals, has_length(0))

    def test_shouldReturnAnApprovalWhenUserIsAuthorizedWithAPermission(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = RawState("state1")
        state2 = RawState("state2")

        authorization_policies = [AuthorizationPolicyBuilder().with_permission(authorized_permission).build()]
        flow = FlowBuilder("my_field", self.content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .build()

        workflow_object = flow.objects[0]

        available_approvals = BasicTestModel.river.my_field.get_available_approvals(as_user=authorized_user)
        assert_that(available_approvals, has_length(1))
        assert_that(list(available_approvals), has_item(
            all_of(
                has_property("workflow_object", workflow_object),
                has_property("workflow", flow.workflow),
                has_property("transition", flow.transitions_metas[0].transitions.first())
            )
        ))

    def test_shouldReturnAnApprovalWhenUserIsAuthorizedWithAUserGroup(self):
        authorized_user_group = GroupObjectFactory()
        authorized_user = UserObjectFactory(groups=[authorized_user_group])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        authorization_policies = [AuthorizationPolicyBuilder().with_group(authorized_user_group).build()]
        flow = FlowBuilder("my_field", self.content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .build()

        workflow_object = flow.objects[0]

        available_approvals = BasicTestModel.river.my_field.get_available_approvals(as_user=authorized_user)
        assert_that(available_approvals, has_length(1))
        assert_that(list(available_approvals), has_item(
            all_of(
                has_property("workflow_object", workflow_object),
                has_property("workflow", flow.workflow),
                has_property("transition", flow.transitions_metas[0].transitions.first())
            )
        ))

    def test__shouldReturnApprovalsOnTimeWhenTooManyWorkflowObject(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = RawState("state1")
        state2 = RawState("state2")

        authorization_policies = [AuthorizationPolicyBuilder().with_permission(authorized_permission).build()]
        FlowBuilder("my_field", self.content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .with_objects(250) \
            .build()

        before = datetime.now()
        approvals = BasicTestModel.river.my_field.get_on_approval_objects(as_user=authorized_user)
        after = datetime.now()
        assert_that(after - before, less_than(timedelta(milliseconds=200)))
        assert_that(approvals, has_length(250))
        print("Time taken %s" % str(after - before))

    def test_shouldAssesInitialStateProperly(self):
        state1 = RawState("state1")
        state2 = RawState("state2")

        flow = FlowBuilder("my_field", self.content_type) \
            .with_transition(state1, state2, []) \
            .build()

        assert_that(BasicTestModel.river.my_field.initial_state, equal_to(flow.get_state(state1)))

    def test_shouldAssesFinalStateProperlyWhenThereIsOnlyOne(self):
        state1 = RawState("state1")
        state2 = RawState("state2")

        flow = FlowBuilder("my_field", self.content_type) \
            .with_transition(state1, state2, []) \
            .build()

        assert_that(BasicTestModel.river.my_field.final_states, has_length(1))
        assert_that(list(BasicTestModel.river.my_field.final_states), has_item(flow.get_state(state2)))

    def test_shouldAssesFinalStateProperlyWhenThereAreMultiple(self):
        state1 = RawState("state1")
        state21 = RawState("state21")
        state22 = RawState("state22")
        state31 = RawState("state31")
        state32 = RawState("state32")

        flow = FlowBuilder("my_field", self.content_type) \
            .with_transition(state1, state21, []) \
            .with_transition(state1, state22, []) \
            .with_transition(state1, state31, []) \
            .with_transition(state1, state32, []) \
            .build()

        assert_that(BasicTestModel.river.my_field.final_states, has_length(4))
        assert_that(
            list(BasicTestModel.river.my_field.final_states),
            has_items(
                flow.get_state(state21),
                flow.get_state(state22),
                flow.get_state(state31),
                flow.get_state(state32)
            )
        )
