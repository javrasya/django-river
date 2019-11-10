from django.contrib.contenttypes.models import ContentType
from hamcrest import equal_to, assert_that, has_entry, none, all_of, has_key, has_length, is_not

from river.models import TransitionApproval
from river.models.factories import PermissionObjectFactory, UserObjectFactory, StateObjectFactory, WorkflowFactory, TransitionApprovalMetaFactory, TransitionMetaFactory
from river.models.hook import AFTER
from river.tests.hooking.base_hooking_test import BaseHookingTest
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory


# noinspection DuplicatedCode
class TransitionHooking(BaseHookingTest):

    def test_shouldInvokeCallbackThatIsRegisteredWithInstanceWhenTransitionHappens(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        content_type = ContentType.objects.get_for_model(BasicTestModel)
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

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        self.hook_post_transition(workflow, transition_meta_2, workflow_object=workflow_object.model)

        assert_that(self.get_output(), none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(self.get_output(), none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.model.pk, transition__source_state=state2, transition__destination_state=state3)

        output = self.get_output()
        assert_that(output, has_length(1))
        assert_that(output[0], has_key("hook"))
        assert_that(output[0]["hook"], has_entry("type", "on-transit"))
        assert_that(output[0]["hook"], has_entry("when", AFTER))
        assert_that(output[0]["hook"], has_entry(
            "payload",
            all_of(
                has_entry(equal_to("workflow_object"), equal_to(workflow_object.model)),
                has_entry(equal_to("transition_approval"), equal_to(last_approval))

            )
        ))

    def test_shouldInvokeCallbackThatIsRegisteredWithoutInstanceWhenTransitionHappens(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        content_type = ContentType.objects.get_for_model(BasicTestModel)
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

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        self.hook_post_transition(workflow, transition_meta_2)

        assert_that(self.get_output(), none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(self.get_output(), none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.model.pk, transition__source_state=state2, transition__destination_state=state3)
        output = self.get_output()
        assert_that(output, has_length(1))
        assert_that(output[0], has_key("hook"))
        assert_that(output[0]["hook"], has_entry("type", "on-transit"))
        assert_that(output[0]["hook"], has_entry("when", AFTER))
        assert_that(output[0]["hook"], has_entry(
            "payload",
            all_of(
                has_entry(equal_to("workflow_object"), equal_to(workflow_object.model)),
                has_entry(equal_to("transition_approval"), equal_to(last_approval))

            )
        ))

    def test_shouldInvokeCallbackForTheOnlyGivenTransition(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        content_type = ContentType.objects.get_for_model(BasicTestModel)
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

        transition_meta_3 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state3,
            destination_state=state1,
        )

        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_3,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        workflow_object.model.river.my_field.approve(as_user=authorized_user)

        assert_that(TransitionApproval.objects.filter(meta=meta1), has_length(2))
        first_approval = TransitionApproval.objects.filter(meta=meta1, transition__iteration=0).first()
        assert_that(first_approval, is_not(none()))

        self.hook_pre_transition(workflow, transition_meta_1, transition=transition_meta_1.transitions.first())

        output = self.get_output()
        assert_that(output, none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)

        output = self.get_output()
        assert_that(output, none())
