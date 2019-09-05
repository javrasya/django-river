from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import equal_to, assert_that, none, has_entry

from river.models import TransitionApproval
from river.models.factories import PermissionObjectFactory, UserObjectFactory, StateObjectFactory, WorkflowFactory, TransitionApprovalMetaFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory

__author__ = 'ahmetdal'


# noinspection DuplicatedCode
class TransitionHooking(TestCase):

    def test_shouldInvokeTheRegisteredViaInstanceApiCallBackWhenATransitionHappens(self):
        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

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
            source_state=state1,
            destination_state=state2,
            priority=1,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        workflow_object.model.river.my_field.hook_post_transition(test_callback)

        assert_that(self.test_args, none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state1))

        assert_that(self.test_args, none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))
        assert_that(self.test_args, equal_to((workflow_object.model, "my_field")))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.model.pk, source_state=state1, destination_state=state2, priority=1)
        assert_that(self.test_kwargs, has_entry(equal_to("transition_approval"), equal_to(last_approval)))

    def test_shouldInvokeTheRegisteredViaClassApiCallBackWhenATransitionHappens(self):
        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

        authorized_permission = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

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
            source_state=state1,
            destination_state=state2,
            priority=1,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        BasicTestModel.river.my_field.hook_post_transition(test_callback)

        assert_that(self.test_args, none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state1))

        assert_that(self.test_args, none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))
        assert_that(self.test_args, equal_to((workflow_object.model, "my_field")))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.model.pk, source_state=state1, destination_state=state2, priority=1)
        assert_that(self.test_kwargs, has_entry(equal_to("transition_approval"), equal_to(last_approval)))

    def test_shouldInvokeTheRegisteredViaInstanceApiCallBackWhenASpecificTransitionHappens(self):
        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

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

        workflow_object.model.river.my_field.hook_post_transition(test_callback, source_state=state2, destination_state=state3)

        assert_that(self.test_args, none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(self.test_args, none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))
        assert_that(self.test_args, equal_to((workflow_object.model, "my_field")))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.model.pk, source_state=state2, destination_state=state3)
        assert_that(self.test_kwargs, has_entry(equal_to("transition_approval"), equal_to(last_approval)))

    def test_shouldInvokeTheRegisteredViaClassApiCallBackWhenASpecificTransitionHappens(self):
        self.test_args = None
        self.test_kwargs = None

        def test_callback(*args, **kwargs):
            self.test_args = args
            self.test_kwargs = kwargs

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

        BasicTestModel.river.my_field.hook_post_transition(test_callback, source_state=state2, destination_state=state3)

        assert_that(self.test_args, none())

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

        assert_that(self.test_args, none())

        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state3))
        assert_that(self.test_args, equal_to((workflow_object.model, "my_field")))

        last_approval = TransitionApproval.objects.get(object_id=workflow_object.model.pk, source_state=state2, destination_state=state3)
        assert_that(self.test_kwargs, has_entry(equal_to("transition_approval"), equal_to(last_approval)))
