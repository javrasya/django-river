from datetime import datetime, timedelta
from unittest import skip

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, equal_to, has_item, all_of, has_property, less_than, has_items, has_length

from river.models import TransitionApproval
from river.models.factories import PermissionObjectFactory, UserObjectFactory, StateObjectFactory, TransitionApprovalMetaFactory, GroupObjectFactory, WorkflowFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ClassApiTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(ClassApiTest, self).__init__(*args, **kwargs)
        self.content_type = ContentType.objects.get_for_model(BasicTestModel)

    def test_shouldReturnNoApprovalWhenUserIsUnAuthorized(self):
        unauthorized_user = UserObjectFactory()

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
        authorized_permission = PermissionObjectFactory()
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        BasicTestModelObjectFactory()

        available_approvals = BasicTestModel.river.my_field.get_available_approvals(as_user=unauthorized_user)
        assert_that(available_approvals, has_length(0))

    def test_shouldReturnAnApprovalWhenUserIsAuthorizedWithAPermission(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        available_approvals = BasicTestModel.river.my_field.get_available_approvals(as_user=authorized_user)
        assert_that(available_approvals, has_length(1))
        assert_that(list(available_approvals), has_item(
            all_of(
                has_property("workflow_object", workflow_object.model),
                has_property("workflow", workflow),
                has_property("source_state", state1),
                has_property("destination_state", state2)
            )
        ))

    def test_shouldReturnAnApprovalWhenUserIsAuthorizedWithAUserGroup(self):
        authorized_user_group = GroupObjectFactory()
        authorized_user = UserObjectFactory(groups=[authorized_user_group])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        approval_meta = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0
        )
        approval_meta.groups.add(authorized_user_group)

        workflow_object = BasicTestModelObjectFactory()

        available_approvals = BasicTestModel.river.my_field.get_available_approvals(as_user=authorized_user)
        assert_that(available_approvals, has_length(1))
        assert_that(list(available_approvals), has_item(
            all_of(
                has_property("workflow_object", workflow_object.model),
                has_property("workflow", workflow),
                has_property("source_state", state1),
                has_property("destination_state", state2)
            )
        ))

    def test_shouldReturnAnApprovalWhenUserIsAuthorizedAsTransactioner(self):
        authorized_user = UserObjectFactory()

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0
        )

        workflow_object = BasicTestModelObjectFactory()

        TransitionApproval.objects.filter(workflow_object=workflow_object.model).update(transactioner=authorized_user)

        available_approvals = BasicTestModel.river.my_field.get_available_approvals(as_user=authorized_user)
        assert_that(available_approvals, has_length(1))
        assert_that(list(available_approvals), has_item(
            all_of(
                has_property("workflow_object", workflow_object.model),
                has_property("workflow", workflow),
                has_property("destination_state", state2)
            )
        ))

    @skip("This test proves the implementation is terrible at scale")
    def test__shouldReturnApprovalsOnTimeWhenTooManyWorkflowObject(self):
        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        self.objects = BasicTestModelObjectFactory.create_batch(250)
        before = datetime.now()
        BasicTestModel.river.my_field.get_on_approval_objects(as_user=authorized_user)
        after = datetime.now()
        assert_that(after - before, less_than(timedelta(milliseconds=100)))
        print("Time taken %s" % str(after - before))

    def test_shouldAssesInitialStateProperly(self):
        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0
        )

        assert_that(BasicTestModel.river.my_field.initial_state, equal_to(state1))

    def test_shouldAssesFinalStateProperlyWhenThereIsOnlyOne(self):
        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0
        )
        assert_that(BasicTestModel.river.my_field.final_states, has_length(1))
        assert_that(list(BasicTestModel.river.my_field.final_states), has_item(state2))

    def test_shouldAssesFinalStateProperlyWhenThereAreMultiple(self):
        state1 = StateObjectFactory(label="state1")
        state21 = StateObjectFactory(label="state21")
        state22 = StateObjectFactory(label="state22")
        state31 = StateObjectFactory(label="state31")
        state32 = StateObjectFactory(label="state32")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state21,
            priority=0
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state22,
            priority=0
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state31,
            priority=0
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state32,
            priority=0
        )

        assert_that(BasicTestModel.river.my_field.final_states, has_length(4))
        assert_that(list(BasicTestModel.river.my_field.final_states), has_items(state21, state22, state31, state32))
