from django.contrib.contenttypes.models import ContentType
from hamcrest import assert_that, equal_to, has_entry, none, has_key

from river.models.factories import PermissionObjectFactory, StateObjectFactory, WorkflowFactory, TransitionApprovalMetaFactory, UserObjectFactory
from river.models.hook import AFTER
from river.tests.hooking.base_hooking_test import BaseHookingTest
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory


# noinspection DuplicatedCode
class CompletedHookingTest(BaseHookingTest):
    def test_shouldInvokeCallbackThatIsRegisteredWithInstanceWhenFlowIsComplete(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        content_type = ContentType.objects.get_for_model(BasicTestModel)
        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state2,
            destination_state=state3,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        self.hook_post_complete(workflow, workflow_object=workflow_object.model)
        assert_that(self.get_output(), none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(self.get_output(), none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))

        output = self.get_output()
        assert_that(output, has_key("hook"))
        assert_that(output["hook"], has_entry("type", "on-complete"))
        assert_that(output["hook"], has_entry("when", AFTER))
        assert_that(output["hook"], has_entry(
            "payload",
            has_entry(equal_to("workflow_object"), equal_to(workflow_object.model))
        ))

    def test_shouldInvokeCallbackThatIsRegisteredWithoutInstanceWhenFlowIsComplete(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        content_type = ContentType.objects.get_for_model(BasicTestModel)
        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state2,
            destination_state=state3,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        self.hook_post_complete(workflow)
        assert_that(self.get_output(), none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))
        assert_that(self.get_output(), none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))

        output = self.get_output()
        assert_that(output, has_key("hook"))
        assert_that(output["hook"], has_entry("type", "on-complete"))
        assert_that(output["hook"], has_entry("when", AFTER))
        assert_that(output["hook"], has_entry(
            "payload",
            has_entry(equal_to("workflow_object"), equal_to(workflow_object.model))
        ))
