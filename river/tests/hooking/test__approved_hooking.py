from django.contrib.contenttypes.models import ContentType
from hamcrest import equal_to, assert_that, none, has_entry, all_of

from river.models.factories import PermissionObjectFactory, UserObjectFactory, StateObjectFactory, WorkflowFactory, TransitionApprovalMetaFactory
from river.tests.hooking.base_hooking_test import BaseHookingTest
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory

__author__ = 'ahmetdal'


# noinspection DuplicatedCode
class ApprovedHooking(BaseHookingTest):

    def test_shouldInvokeCallbackThatIsRegisteredWithInstanceWhenAnApprovingHappens(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        content_type = ContentType.objects.get_for_model(BasicTestModel)
        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")
        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=1,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        self.hook_pre_approve(workflow, meta1, workflow_object=workflow_object.model)

        assert_that(self.get_output(), none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state1))

        assert_that(
            self.get_output(), has_entry(
                "kwargs",
                all_of(
                    has_entry(equal_to("workflow_object"), equal_to(workflow_object.model)),
                    has_entry(equal_to("transition_approval"), equal_to(meta1.transition_approvals.filter(priority=0).first()))

                )
            )
        )

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(
            self.get_output(), has_entry(
                "kwargs",
                all_of(
                    has_entry(equal_to("workflow_object"), equal_to(workflow_object.model)),
                    has_entry(equal_to("transition_approval"), equal_to(meta1.transition_approvals.filter(priority=0).first()))

                )
            )
        )

    def test_shouldInvokeCallbackThatIsRegisteredWithoutInstanceWhenAnApprovingHappens(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        content_type = ContentType.objects.get_for_model(BasicTestModel)
        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="my_field")
        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=1,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        self.hook_pre_approve(workflow, meta1)

        assert_that(self.get_output(), none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state1))

        assert_that(
            self.get_output(), has_entry(
                "kwargs",
                all_of(
                    has_entry(equal_to("workflow_object"), equal_to(workflow_object.model)),
                    has_entry(equal_to("transition_approval"), equal_to(meta1.transition_approvals.filter(priority=0).first()))

                )
            )
        )

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(
            self.get_output(), has_entry(
                "kwargs",
                all_of(
                    has_entry(equal_to("workflow_object"), equal_to(workflow_object.model)),
                    has_entry(equal_to("transition_approval"), equal_to(meta1.transition_approvals.filter(priority=0).first()))

                )
            )
        )
