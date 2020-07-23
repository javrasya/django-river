from django.contrib.contenttypes.models import ContentType
from hamcrest import assert_that, equal_to, has_entry, none, has_key, has_length

from river.models.factories import PermissionObjectFactory, StateObjectFactory, UserObjectFactory
from river.models.hook import AFTER
from river.tests.hooking.base_hooking_test import BaseHookingTest
from river.tests.models import BasicTestModel
# noinspection DuplicatedCode
from rivertest.flowbuilder import AuthorizationPolicyBuilder, FlowBuilder, RawState


class CompletedHookingTest(BaseHookingTest):
    def test_shouldInvokeCallbackThatIsRegisteredWithInstanceWhenFlowIsComplete(self):
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

        self.hook_post_complete(flow.workflow, workflow_object=workflow_object)
        assert_that(self.get_output(), none())

        assert_that(workflow_object.my_field, equal_to(flow.get_state(state1)))
        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state2)))

        assert_that(self.get_output(), none())

        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state3)))

        output = self.get_output()
        assert_that(output, has_length(1))
        assert_that(output[0], has_key("hook"))
        assert_that(output[0]["hook"], has_entry("type", "on-complete"))
        assert_that(output[0]["hook"], has_entry("when", AFTER))
        assert_that(output[0]["hook"], has_entry(
            "payload",
            has_entry(equal_to("workflow_object"), equal_to(workflow_object))
        ))

    def test_shouldInvokeCallbackThatIsRegisteredWithoutInstanceWhenFlowIsComplete(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])
        content_type = ContentType.objects.get_for_model(BasicTestModel)

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        authorization_policies = [
            AuthorizationPolicyBuilder().with_permission(authorized_permission).build(),
        ]
        flow = FlowBuilder("my_field", content_type) \
            .with_transition(state1, state2, authorization_policies) \
            .with_transition(state2, state3, authorization_policies) \
            .build()

        workflow_object = flow.objects[0]

        self.hook_post_complete(flow.workflow)
        assert_that(self.get_output(), none())

        assert_that(workflow_object.my_field, equal_to(flow.get_state(state1)))
        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state2)))
        assert_that(self.get_output(), none())

        workflow_object.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.my_field, equal_to(flow.get_state(state3)))

        output = self.get_output()
        assert_that(output, has_length(1))
        assert_that(output[0], has_key("hook"))
        assert_that(output[0]["hook"], has_entry("type", "on-complete"))
        assert_that(output[0]["hook"], has_entry("when", AFTER))
        assert_that(output[0]["hook"], has_entry(
            "payload",
            has_entry(equal_to("workflow_object"), equal_to(workflow_object))
        ))
