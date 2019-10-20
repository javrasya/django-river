from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, equal_to, has_item, has_property, raises, calling, has_length, is_not, all_of, none

from river.models import TransitionApproval, PENDING, CANCELLED, APPROVED
from river.models.factories import UserObjectFactory, StateObjectFactory, TransitionApprovalMetaFactory, PermissionObjectFactory, WorkflowFactory
from river.tests.matchers import has_permission
from river.tests.models import BasicTestModel, ModelWithTwoStateFields
from river.tests.models.factories import BasicTestModelObjectFactory, ModelWithTwoStateFieldsObjectFactory
from river.utils.exceptions import RiverException


# noinspection PyMethodMayBeStatic,DuplicatedCode
class InstanceApiTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(InstanceApiTest, self).__init__(*args, **kwargs)
        self.content_type = ContentType.objects.get_for_model(BasicTestModel)

    def test_shouldNotReturnOtherObjectsApprovalsForTheAuthorizedUser(self):
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

        workflow_object1 = BasicTestModelObjectFactory()
        workflow_object2 = BasicTestModelObjectFactory()

        available_approvals = workflow_object1.model.river.my_field.get_available_approvals(as_user=authorized_user)
        assert_that(available_approvals, has_length(1))
        assert_that(list(available_approvals), has_item(
            has_property("workflow_object", workflow_object1.model)
        ))
        assert_that(list(available_approvals), has_item(
            is_not(has_property("workflow_object", workflow_object2.model))
        ))

    def test_shouldNotAllowUnauthorizedUserToProceedToNextState(self):
        unauthorized_user = UserObjectFactory()

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        authorized_permission = PermissionObjectFactory()

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(
            calling(workflow_object.model.river.my_field.approve).with_args(as_user=unauthorized_user),
            raises(RiverException, "There is no available approval for the user")
        )

    def test_shouldAllowAuthorizedUserToProceedToNextState(self):
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

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(state2))

    def test_shouldNotLetUserWhosePriorityComesLaterApproveProceed(self):
        manager_permission = PermissionObjectFactory()
        team_leader_permission = PermissionObjectFactory()

        manager = UserObjectFactory(user_permissions=[manager_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=1,
            permissions=[manager_permission]

        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[team_leader_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(
            calling(workflow_object.model.river.my_field.approve).with_args(as_user=manager),
            raises(RiverException, "There is no available approval for the user")
        )

    def test_shouldNotTransitToNextStateWhenThereAreMultipleApprovalsToBeApproved(self):
        manager_permission = PermissionObjectFactory()
        team_leader_permission = PermissionObjectFactory()

        team_leader = UserObjectFactory(user_permissions=[team_leader_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=1,
            permissions=[manager_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[team_leader_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(team_leader)
        assert_that(workflow_object.model.my_field, equal_to(state1))

    def test_shouldTransitToNextStateWhenAppTheApprovalsAreApprovedBeApproved(self):
        manager_permission = PermissionObjectFactory()
        team_leader_permission = PermissionObjectFactory()

        manager = UserObjectFactory(user_permissions=[manager_permission])
        team_leader = UserObjectFactory(user_permissions=[team_leader_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=1,
            permissions=[manager_permission]

        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[team_leader_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(team_leader)
        assert_that(workflow_object.model.my_field, equal_to(state1))

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(manager)
        assert_that(workflow_object.model.my_field, equal_to(state2))

    def test_shouldDictatePassingNextStateWhenThereAreMultiple(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
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
            destination_state=state3,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(
            calling(workflow_object.model.river.my_field.approve).with_args(as_user=authorized_user),
            raises(RiverException, "State must be given when there are multiple states for destination")
        )

    def test_shouldTransitToTheGivenNextStateWhenThereAreMultipleNextStates(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
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
            destination_state=state3,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=state3)
        assert_that(workflow_object.model.my_field, equal_to(state3))

    def test_shouldNotAcceptANextStateWhichIsNotAmongPossibleNextStates(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")
        invalid_state = StateObjectFactory(label="state4")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
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
            destination_state=state3,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(
            calling(workflow_object.model.river.my_field.approve).with_args(as_user=authorized_user, next_state=invalid_state),
            raises(RiverException,
                   "Invalid state is given\(%s\). Valid states is\(are\) (%s|%s)" % (
                       invalid_state.label,
                       ",".join([state2.label, state3.label]),
                       ",".join([state3.label, state2.label]))
                   )
        )

    def test_shouldAllowCyclicTransitions(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        cycle_state_1 = StateObjectFactory(label="cycle_state_1")
        cycle_state_2 = StateObjectFactory(label="cycle_state_2")
        cycle_state_3 = StateObjectFactory(label="cycle_state_3")
        off_the_cycle_state = StateObjectFactory(label="off_the_cycle_state")

        workflow = WorkflowFactory(initial_state=cycle_state_1, content_type=self.content_type, field_name="my_field")

        meta_1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_1,
            destination_state=cycle_state_2,
            priority=0,
            permissions=[authorized_permission]
        )

        meta_2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_2,
            destination_state=cycle_state_3,
            priority=0,
            permissions=[authorized_permission]
        )

        meta_3 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=cycle_state_1,
            priority=0,
            permissions=[authorized_permission]
        )

        final_meta = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=off_the_cycle_state,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_2))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_3))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(4))

        assert_that(approvals, has_item(
            is_not(
                all_of(
                    has_property("source_state", meta_1.source_state),
                    has_property("destination_state", meta_1.destination_state),
                    has_permission("permissions", has_length(1)),
                    has_permission("permissions", has_item(authorized_permission)),
                    has_property("status", PENDING),
                )
            )
        ))

        assert_that(approvals, has_item(
            is_not(
                all_of(
                    has_property("source_state", meta_2.source_state),
                    has_property("destination_state", meta_2.destination_state),
                    has_permission("permissions", has_length(1)),
                    has_permission("permissions", has_item(authorized_permission)),
                    has_property("status", PENDING),
                )
            )
        ))

        assert_that(approvals, has_item(
            is_not(
                all_of(
                    has_property("source_state", meta_3.source_state),
                    has_property("destination_state", meta_3.destination_state),
                    has_permission("permissions", has_length(1)),
                    has_permission("permissions", has_item(authorized_permission)),
                    has_property("status", PENDING),
                )
            )
        ))

        assert_that(approvals, has_item(
            is_not(
                all_of(
                    has_property("source_state", meta_3.source_state),
                    has_property("destination_state", final_meta.destination_state),
                    has_permission("permissions", has_length(1)),
                    has_permission("permissions", has_item(authorized_permission)),
                    has_property("status", PENDING),
                )
            )
        ))

        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=cycle_state_1)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(8))

        assert_that(approvals, has_item(
            all_of(
                has_property("source_state", meta_1.source_state),
                has_property("destination_state", meta_1.destination_state),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_property("source_state", meta_2.source_state),
                has_property("destination_state", meta_2.destination_state),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_property("source_state", meta_3.source_state),
                has_property("destination_state", meta_3.destination_state),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            is_not(
                all_of(
                    has_property("source_state", meta_3.source_state),
                    has_property("destination_state", final_meta.destination_state),
                    has_permission("permissions", has_length(1)),
                    has_permission("permissions", has_item(authorized_permission)),
                    has_property("status", CANCELLED),
                )
            )
        ))

        assert_that(approvals, has_item(
            is_not(
                all_of(
                    has_property("source_state", meta_3.source_state),
                    has_property("destination_state", final_meta.destination_state),
                    has_permission("permissions", has_length(1)),
                    has_permission("permissions", has_item(authorized_permission)),
                    has_property("status", PENDING),
                )
            )
        ))

    def test__shouldHandleUndefinedSecondWorkflowCase(self):
        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        content_type = ContentType.objects.get_for_model(ModelWithTwoStateFields)
        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="status1")
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
        )

        workflow_object = ModelWithTwoStateFieldsObjectFactory()

        assert_that(workflow_object.model.status1, equal_to(state1))
        assert_that(workflow_object.model.status2, none())

    def test__shouldReturnNextApprovals(self):
        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
        )

        meta2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state3,
            priority=0,
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(state1))
        next_approvals = workflow_object.model.river.my_field.next_approvals
        assert_that(next_approvals, has_length(2))
        assert_that(next_approvals, has_item(meta1.transition_approvals.first()))
        assert_that(next_approvals, has_item(meta2.transition_approvals.first()))

    def test_shouldCancelAllOtherStateTransition(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")
        state4 = StateObjectFactory(label="state4")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")
        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
            priority=0,
            permissions=[authorized_permission]
        )

        meta2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state3,
            priority=0,
            permissions=[authorized_permission]
        )

        meta3 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state4,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(state1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=state3)
        assert_that(workflow_object.model.my_field, equal_to(state3))

        assert_that(
            meta2.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", APPROVED))
            )
        ),

        assert_that(
            meta1.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", CANCELLED))
            )
        ),

        assert_that(
            meta3.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", CANCELLED))
            )
        )
