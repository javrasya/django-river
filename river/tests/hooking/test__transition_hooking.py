from django.contrib.contenttypes.models import ContentType
from hamcrest import equal_to, assert_that, has_entry, none, all_of, has_key, has_length, is_not

from river.models import TransitionApproval
from river.models.factories import PermissionObjectFactory, UserObjectFactory
from river.models.hook import AFTER
from river.tests.hooking.base_hooking_test import BaseHookingTest
from river.tests.models import BasicTestModel
# noinspection DuplicatedCode
from rivertest.flowbuilder import AuthorizationPolicyBuilder, FlowBuilder, RawState


class TransitionHooking(BaseHookingTest):

    def test_shouldInvokeCallbackThatIsRegisteredWithInstanceWhenTransitionHappens(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = RawState("state1")
        state2 = RawState("state2")
        state3 = RawState("state3")

        authorization_policies = [
            AuthorizationPolicyBuilder().with_permission(authorized_permission).build(),
        ]
        flow = FlowBuilder("my_field", content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .with_transition(state2, state3, authorization_policies) \
            .build()

        workflow_object = flow.objects[0]

        self.hook_post_transition(flow.workflow, flow.transitions_metas[1], workflow_object=workflow_object)

        assert_that(self.get_output(), none())

        assert_that(workflow_object.my_field, equal_to(flow.get_state(state1)))
        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state2)))

        assert_that(self.get_output(), none())

        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state3)))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.pk, transition__source_state=flow.get_state(state2), transition__destination_state=flow.get_state(state3))

        output = self.get_output()
        assert_that(output, has_length(1))
        assert_that(output[0], has_key("hook"))
        assert_that(output[0]["hook"], has_entry("type", "on-transit"))
        assert_that(output[0]["hook"], has_entry("when", AFTER))
        assert_that(output[0]["hook"], has_entry(
            "payload",
            all_of(
                has_entry(equal_to("workflow_object"), equal_to(workflow_object)),
                has_entry(equal_to("transition_approval"), equal_to(last_approval))

            )
        ))

    def test_shouldInvokeCallbackThatIsRegisteredWithoutInstanceWhenTransitionHappens(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = RawState("state1")
        state2 = RawState("state2")
        state3 = RawState("state3")

        authorization_policies = [
            AuthorizationPolicyBuilder().with_permission(authorized_permission).build(),
        ]
        flow = FlowBuilder("my_field", content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .with_transition(state2, state3, authorization_policies) \
            .build()

        workflow_object = flow.objects[0]

        self.hook_post_transition(flow.workflow, flow.transitions_metas[1])

        assert_that(self.get_output(), none())

        assert_that(workflow_object.my_field, equal_to(flow.get_state(state1)))
        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state2)))

        assert_that(self.get_output(), none())

        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state3)))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.pk, transition__source_state=flow.get_state(state2), transition__destination_state=flow.get_state(state3))
        output = self.get_output()
        assert_that(output, has_length(1))
        assert_that(output[0], has_key("hook"))
        assert_that(output[0]["hook"], has_entry("type", "on-transit"))
        assert_that(output[0]["hook"], has_entry("when", AFTER))
        assert_that(output[0]["hook"], has_entry(
            "payload",
            all_of(
                has_entry(equal_to("workflow_object"), equal_to(workflow_object)),
                has_entry(equal_to("transition_approval"), equal_to(last_approval))

            )
        ))

    def test_shouldInvokeCallbackForTheOnlyGivenTransition(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = RawState("state1")
        state2 = RawState("state2")
        state3 = RawState("state3")

        authorization_policies = [
            AuthorizationPolicyBuilder().with_permission(authorized_permission).build(),
        ]
        flow = FlowBuilder("my_field", content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .with_transition(state2, state3, authorization_policies) \
            .with_transition(state3, state1, authorization_policies) \
            .build()

        workflow_object = flow.objects[0]

        workflow_object.river.my_field.approve(as_user=authorized_user)
        workflow_object.river.my_field.approve(as_user=authorized_user)
        workflow_object.river.my_field.approve(as_user=authorized_user)

        assert_that(TransitionApproval.objects.filter(meta=flow.transitions_approval_metas[0]), has_length(2))
        first_approval = TransitionApproval.objects.filter(meta=flow.transitions_approval_metas[0], transition__iteration=0).first()
        assert_that(first_approval, is_not(none()))

        self.hook_pre_transition(flow.workflow, flow.transitions_metas[0], transition=flow.transitions_metas[0].transitions.first())

        output = self.get_output()
        assert_that(output, none())

        workflow_object.river.my_field.approve(as_user=authorized_user)

        output = self.get_output()
        assert_that(output, none())
