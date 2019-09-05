from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, equal_to, none

from river.models.factories import PermissionObjectFactory, StateObjectFactory, WorkflowFactory, TransitionApprovalMetaFactory, UserObjectFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory

__author__ = 'ahmetdal'


# noinspection DuplicatedCode
class CompletedHookingTest(TestCase):
    def setUp(self):
        super(CompletedHookingTest, self).setUp()

    def test_shouldInvokeTheRegisteredViaInstanceApiCallBackWhenFlowIsCompleteForTheObject(self):
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

        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        workflow_object.model.river.my_field.hook_post_complete(test_callback)

        assert_that(self.test_args, none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(self.test_args, none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))

        assert_that(self.test_args, equal_to((workflow_object.model, "my_field")))

    def test_shouldInvokeTheRegisteredViaClassApiCallBackWhenFlowIsCompleteForTheObject(self):
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

        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        BasicTestModel.river.my_field.hook_post_complete(test_callback)

        assert_that(self.test_args, none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(self.test_args, none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))

        assert_that(self.test_args, equal_to((workflow_object.model, "my_field")))
