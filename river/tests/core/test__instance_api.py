from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, equal_to, has_item, has_property, raises, calling, has_length, is_not, all_of, none, has_items

from river.models import TransitionApproval, PENDING, CANCELLED, APPROVED, Transition, JUMPED
from river.models.factories import UserObjectFactory, StateObjectFactory, TransitionApprovalMetaFactory, PermissionObjectFactory, WorkflowFactory, \
    TransitionMetaFactory
from river.tests.matchers import has_permission, has_transition
from river.tests.models import BasicTestModel, ModelWithTwoStateFields, ModelWithStringPrimaryKey
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
        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
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
        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
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

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
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

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
            priority=1,
            permissions=[manager_permission]

        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
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

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
            priority=1,
            permissions=[manager_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
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

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
            priority=1,
            permissions=[manager_permission]

        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
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

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
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
        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
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

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
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
        final_state = StateObjectFactory(label="final_state")

        workflow = WorkflowFactory(initial_state=cycle_state_1, content_type=self.content_type, field_name="my_field")

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_1,
            destination_state=cycle_state_2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_2,
            destination_state=cycle_state_3,
        )

        transition_meta_3 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=cycle_state_1,
        )

        transition_meta_4 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=off_the_cycle_state,
        )

        transition_meta_5 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=off_the_cycle_state,
            destination_state=final_state,
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

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_3,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_4,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_5,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_2))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_3))

        transitions = Transition.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(transitions, has_length(5))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(5))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_1, cycle_state_2, iteration=0),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_2, cycle_state_3, iteration=1),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, cycle_state_1, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, off_the_cycle_state, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(off_the_cycle_state, final_state, iteration=3),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=cycle_state_1)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))

        transitions = Transition.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(transitions, has_length(10))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(10))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_1, cycle_state_2, iteration=0),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_2, cycle_state_3, iteration=1),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, cycle_state_1, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, off_the_cycle_state, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", CANCELLED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(off_the_cycle_state, final_state, iteration=3),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", CANCELLED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_1, cycle_state_2, iteration=3),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_2, cycle_state_3, iteration=4),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, cycle_state_1, iteration=5),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, off_the_cycle_state, iteration=5),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(off_the_cycle_state, final_state, iteration=6),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

    def test_shouldHandleSecondCycleProperly(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        cycle_state_1 = StateObjectFactory(label="cycle_state_1")
        cycle_state_2 = StateObjectFactory(label="cycle_state_2")
        cycle_state_3 = StateObjectFactory(label="cycle_state_3")
        off_the_cycle_state = StateObjectFactory(label="off_the_cycle_state")
        final_state = StateObjectFactory(label="final_state")

        workflow = WorkflowFactory(initial_state=cycle_state_1, content_type=self.content_type, field_name="my_field")

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_1,
            destination_state=cycle_state_2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_2,
            destination_state=cycle_state_3,
        )

        transition_meta_3 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=cycle_state_1,
        )

        transition_meta_4 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=off_the_cycle_state,
        )

        transition_meta_5 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=off_the_cycle_state,
            destination_state=final_state,
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

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_3,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_4,
            priority=0,
            permissions=[authorized_permission]
        )

        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_5,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_2))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_3))

        transitions = Transition.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(transitions, has_length(5))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(5))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_1, cycle_state_2, iteration=0),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_2, cycle_state_3, iteration=1),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, cycle_state_1, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, off_the_cycle_state, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(off_the_cycle_state, final_state, iteration=3),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=cycle_state_1)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_2))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_3))
        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=cycle_state_1)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(15))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_1, cycle_state_2, iteration=0),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_2, cycle_state_3, iteration=1),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, cycle_state_1, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, off_the_cycle_state, iteration=2),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", CANCELLED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(off_the_cycle_state, final_state, iteration=3),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", CANCELLED),
            )

        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_1, cycle_state_2, iteration=3),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_2, cycle_state_3, iteration=4),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, cycle_state_1, iteration=5),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", APPROVED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, off_the_cycle_state, iteration=5),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", CANCELLED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(off_the_cycle_state, final_state, iteration=6),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", CANCELLED),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_1, cycle_state_2, iteration=6),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_2, cycle_state_3, iteration=7),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, cycle_state_1, iteration=8),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(cycle_state_3, off_the_cycle_state, iteration=8),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

        assert_that(approvals, has_item(
            all_of(
                has_transition(off_the_cycle_state, final_state, iteration=9),
                has_permission("permissions", has_length(1)),
                has_permission("permissions", has_item(authorized_permission)),
                has_property("status", PENDING),
            )
        ))

    def test__shouldHandleUndefinedSecondWorkflowCase(self):
        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        content_type = ContentType.objects.get_for_model(ModelWithTwoStateFields)
        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="status1")

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
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

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state3,
        )

        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
        )

        meta2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
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

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state3,
        )

        transition_meta_3 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state4,
        )

        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission]
        )

        meta2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission]
        )

        meta3 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_3,
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

    def test_shouldCancelAllOtherStateTransitionDescendants(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")
        state4 = StateObjectFactory(label="state4")
        state5 = StateObjectFactory(label="state5")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state3,
        )

        transition_meta_3 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state4,
        )

        transition_meta_4 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state4,
            destination_state=state5,
        )

        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission]
        )

        meta2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission]
        )

        meta3 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_3,
            priority=0,
            permissions=[authorized_permission]
        )

        meta4 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_4,
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

        assert_that(
            meta4.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", CANCELLED))
            )
        )

    def test_shouldNotCancelDescendantsIfItIsPartOfPossibleFuture(self):
        authorized_permission = PermissionObjectFactory()

        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])

        first_state = StateObjectFactory(label="first")
        diamond_left_state_1 = StateObjectFactory(label="diamond-left-1")
        diamond_left_state_2 = StateObjectFactory(label="diamond-left-2")
        diamond_right_state_1 = StateObjectFactory(label="diamond-right-1")
        diamond_right_state_2 = StateObjectFactory(label="diamond-right-2")
        diamond_join_state = StateObjectFactory(label="diamond-join")
        final_state = StateObjectFactory(label="final")

        workflow = WorkflowFactory(initial_state=first_state, content_type=self.content_type, field_name="my_field")

        first_to_left_transition = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=first_state,
            destination_state=diamond_left_state_1,
        )

        first_to_right_transition = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=first_state,
            destination_state=diamond_right_state_1,
        )

        left_follow_up_transition = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=diamond_left_state_1,
            destination_state=diamond_left_state_2,
        )

        right_follow_up_transition = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=diamond_right_state_1,
            destination_state=diamond_right_state_2,
        )

        left_join_transition = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=diamond_left_state_2,
            destination_state=diamond_join_state
        )

        right_join_transition = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=diamond_right_state_2,
            destination_state=diamond_join_state
        )

        join_to_final_transition = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=diamond_join_state,
            destination_state=final_state
        )

        first_to_left = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=first_to_left_transition,
            priority=0,
            permissions=[authorized_permission]
        )

        first_to_right = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=first_to_right_transition,
            priority=0,
            permissions=[authorized_permission]
        )

        left_follow_up = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=left_follow_up_transition,
            priority=0,
            permissions=[authorized_permission]
        )

        right_follow_up = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=right_follow_up_transition,
            priority=0,
            permissions=[authorized_permission]
        )

        left_join = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=left_join_transition,
            priority=0,
            permissions=[authorized_permission]
        )

        right_join = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=right_join_transition,
            priority=0,
            permissions=[authorized_permission]
        )

        join_to_final = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=join_to_final_transition,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(first_state))
        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=diamond_left_state_1)
        assert_that(workflow_object.model.my_field, equal_to(diamond_left_state_1))

        assert_that(
            first_to_left.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", APPROVED))
            )
        ),

        assert_that(
            left_follow_up.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", PENDING))
            )
        )

        assert_that(
            left_join.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", PENDING))
            )
        )

        assert_that(
            first_to_right.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", CANCELLED))
            )
        ),

        assert_that(
            right_follow_up.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", CANCELLED))
            )
        )

        assert_that(
            right_join.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", CANCELLED))
            )
        )

        assert_that(
            join_to_final.transition_approvals.all(),
            all_of(
                has_length(1),
                has_item(has_property("status", PENDING))
            )
        )

    def test_shouldAssessIterationsCorrectly(self):
        authorized_permission1 = PermissionObjectFactory()
        authorized_permission2 = PermissionObjectFactory()

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

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

        meta1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission1]
        )

        meta2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission1]
        )

        meta3 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=1,
            permissions=[authorized_permission2]
        )

        workflow_object = BasicTestModelObjectFactory()

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(3))
        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta1),
                    has_transition(state1, state2, iteration=0)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta2),
                    has_transition(state2, state3, iteration=1),
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta3),
                    has_transition(state2, state3, iteration=1),
                )
            )
        )

    def test_shouldAssessIterationsCorrectlyWhenCycled(self):
        authorized_permission1 = PermissionObjectFactory()
        authorized_permission2 = PermissionObjectFactory()
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission1, authorized_permission2])

        cycle_state_1 = StateObjectFactory(label="cycle_state_1")
        cycle_state_2 = StateObjectFactory(label="cycle_state_2")
        cycle_state_3 = StateObjectFactory(label="cycle_state_3")
        off_the_cycle_state = StateObjectFactory(label="off_the_cycle_state")
        final_state = StateObjectFactory(label="final_state")

        workflow = WorkflowFactory(initial_state=cycle_state_1, content_type=self.content_type, field_name="my_field")

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_1,
            destination_state=cycle_state_2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_2,
            destination_state=cycle_state_3,
        )

        transition_meta_3 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=cycle_state_1,
        )

        transition_meta_4 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=cycle_state_3,
            destination_state=off_the_cycle_state,
        )

        transition_meta_5 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=off_the_cycle_state,
            destination_state=final_state,
        )

        meta_1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission1]
        )

        meta_21 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission1]
        )

        meta_22 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=1,
            permissions=[authorized_permission2]
        )

        meta_3 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_3,
            priority=0,
            permissions=[authorized_permission1]
        )

        meta_4 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_4,
            priority=0,
            permissions=[authorized_permission1]
        )

        final_meta = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_5,
            priority=0,
            permissions=[authorized_permission1]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_2))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_2))
        workflow_object.model.river.my_field.approve(as_user=authorized_user)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_3))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(6))

        workflow_object.model.river.my_field.approve(as_user=authorized_user, next_state=cycle_state_1)
        assert_that(workflow_object.model.my_field, equal_to(cycle_state_1))

        approvals = TransitionApproval.objects.filter(workflow=workflow, workflow_object=workflow_object.model)
        assert_that(approvals, has_length(12))

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_1),
                    has_transition(cycle_state_1, cycle_state_2, iteration=0)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_21),
                    has_transition(cycle_state_2, cycle_state_3, iteration=1)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_22),
                    has_transition(cycle_state_2, cycle_state_3, iteration=1)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_3),
                    has_transition(cycle_state_3, cycle_state_1, iteration=2)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_4),
                    has_transition(cycle_state_3, off_the_cycle_state, iteration=2)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", final_meta),
                    has_transition(off_the_cycle_state, final_state, iteration=3)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_1),
                    has_transition(cycle_state_1, cycle_state_2, iteration=3)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_21),
                    has_transition(cycle_state_2, cycle_state_3, iteration=4)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_22),
                    has_transition(cycle_state_2, cycle_state_3, iteration=4)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_3),
                    has_transition(cycle_state_3, cycle_state_1, iteration=5)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", meta_4),
                    has_transition(cycle_state_3, off_the_cycle_state, iteration=5)
                )
            )
        )

        assert_that(
            approvals, has_item(
                all_of(
                    has_property("meta", final_meta),
                    has_transition(off_the_cycle_state, final_state, iteration=6)
                )
            )
        )

    def test_shouldJumpToASpecificState(self):
        authorized_permission = PermissionObjectFactory()

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

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

        transition_approval_meta_1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission]
        )

        transition_approval_meta_2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(state1))
        assert_that(
            Transition.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_meta_1),
                ),
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_meta_2),
                )
            )
        )

        assert_that(
            TransitionApproval.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_approval_meta_1),
                ),
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_approval_meta_2),
                )
            )
        )

        workflow_object.model.river.my_field.jump_to(state3)

        assert_that(workflow_object.model.my_field, equal_to(state3))
        assert_that(
            Transition.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_meta_1),
                ),
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_meta_2),
                )
            )
        )

        assert_that(
            TransitionApproval.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_approval_meta_1),
                ),
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_approval_meta_2),
                )
            )
        )

    def test_shouldJumpToASpecificStateWhenThereAreMultipleNextState(self):
        authorized_permission = PermissionObjectFactory()

        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")
        state3 = StateObjectFactory(label="state3")

        workflow = WorkflowFactory(initial_state=state1, content_type=self.content_type, field_name="my_field")

        transition_meta_1 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )

        transition_meta_2 = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state3,
        )

        transition_approval_meta_1 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_1,
            priority=0,
            permissions=[authorized_permission]
        )

        transition_approval_meta_2 = TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta_2,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = BasicTestModelObjectFactory()

        assert_that(workflow_object.model.my_field, equal_to(state1))
        assert_that(
            Transition.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_meta_1),
                ),
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_meta_2),
                )
            )
        )

        assert_that(
            TransitionApproval.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_approval_meta_1),
                ),
                all_of(
                    has_property("status", PENDING),
                    has_property("meta", transition_approval_meta_2),
                )
            )
        )

        workflow_object.model.river.my_field.jump_to(state3)

        assert_that(workflow_object.model.my_field, equal_to(state3))
        assert_that(
            Transition.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_meta_1),
                ),
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_meta_2),
                )
            )
        )

        assert_that(
            TransitionApproval.objects.filter(workflow_object=workflow_object.model),
            has_items(
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_approval_meta_1),
                ),
                all_of(
                    has_property("status", JUMPED),
                    has_property("meta", transition_approval_meta_2),
                )
            )
        )

    def test_shouldNotCrashWhenAModelObjectWithStringPrimaryKeyIsApproved(self):
        state1 = StateObjectFactory(label="state1")
        state2 = StateObjectFactory(label="state2")

        content_type = ContentType.objects.get_for_model(ModelWithStringPrimaryKey)
        authorized_permission = PermissionObjectFactory(content_type=content_type)
        authorized_user = UserObjectFactory(user_permissions=[authorized_permission])
        workflow = WorkflowFactory(initial_state=state1, content_type=content_type, field_name="status")

        transition_meta = TransitionMetaFactory.create(
            workflow=workflow,
            source_state=state1,
            destination_state=state2,
        )
        TransitionApprovalMetaFactory.create(
            workflow=workflow,
            transition_meta=transition_meta,
            priority=0,
            permissions=[authorized_permission]
        )

        workflow_object = ModelWithStringPrimaryKey.objects.create()

        assert_that(workflow_object.status, equal_to(state1))
        workflow_object.river.status.approve(as_user=authorized_user)
        assert_that(workflow_object.status, equal_to(state2))
