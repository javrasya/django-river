from collections import namedtuple

from django.db import transaction

from river.models import State, Workflow
from river.models.factories import TransitionMetaFactory, TransitionApprovalMetaFactory
from river.tests.models.factories import BasicTestModelObjectFactory

RawTransition = namedtuple("RawTransition", ["source_state", "destination_state", "authorization_policies"])
RawState = namedtuple("RawState", ["label"])
AuthorizationPolicy = namedtuple("RawAuthorizationPolicy", ["priority", "permissions", "groups", "user"])


class Flow(object):
    def __init__(self, workflow, states, transitions_metas, transitions_approval_metas, objects):
        self.workflow = workflow
        self.states = states
        self.transitions_metas = transitions_metas
        self.transitions_approval_metas = transitions_approval_metas
        self.objects = objects

    def get_state(self, raw_state):
        return self.states[raw_state.label]


class AuthorizationPolicyBuilder(object):

    def __init__(self):
        self._priority = 0
        self._user = None
        self._permissions = []
        self._groups = []

    def with_priority(self, priority):
        self._priority = priority
        return self

    def with_permission(self, permission):
        return self.with_permissions([permission])

    def with_user(self, user):
        self._user = user
        return self

    def with_group(self, group):
        return self.with_groups([group])

    def with_permissions(self, permissions):
        self._permissions.extend(permissions)
        return self

    def with_groups(self, groups):
        self._groups.extend(groups)
        return self

    def build(self):
        return AuthorizationPolicy(self._priority, self._permissions, self._groups, self._user)


class FlowBuilder(object):

    def __init__(self, field_name, content_type):
        self.field_name = field_name
        self.content_type = content_type
        self.raw_transitions = []
        self.additional_raw_states = []
        self.objects_count = 1
        self.object_factory = lambda: BasicTestModelObjectFactory().model

    def with_transition(self, source_state, destination_state, authorization_policies=None):
        self.raw_transitions.append(RawTransition(source_state, destination_state, authorization_policies))
        return self

    def with_additional_state(self, state):
        self.additional_raw_states.append(state)
        return self

    def with_objects(self, count):
        self.objects_count = count
        return self

    def with_object_factory(self, factory):
        self.object_factory = factory
        return self

    @transaction.atomic
    def build(self):
        workflow = None
        states = {}
        transition_metas = []
        transitions_approval_metas = []
        workflow_objects = []
        for additional_raw_state in self.additional_raw_states:
            state, _ = State.objects.get_or_create(label=additional_raw_state.label)
            states[state.label] = state

        for raw_transition in self.raw_transitions:
            source_state, _ = State.objects.get_or_create(label=raw_transition.source_state.label)
            if not workflow:
                workflow = Workflow.objects.create(field_name=self.field_name, content_type=self.content_type, initial_state=source_state)
            destination_state, _ = State.objects.get_or_create(label=raw_transition.destination_state.label)

            states[source_state.label] = source_state
            states[destination_state.label] = destination_state

            transition_meta = TransitionMetaFactory.create(
                workflow=workflow,
                source_state=source_state,
                destination_state=destination_state,
            )
            transition_metas.append(transition_meta)

            if raw_transition.authorization_policies:
                for authorization_policy in raw_transition.authorization_policies:
                    transition_approval_meta = TransitionApprovalMetaFactory.create(
                        workflow=workflow,
                        transition_meta=transition_meta,
                        priority=authorization_policy.priority,
                        permissions=authorization_policy.permissions,
                    )
                    transition_approval_meta.groups.set(authorization_policy.groups)
                    transitions_approval_metas.append(transition_approval_meta)

        for i in range(self.objects_count):
            workflow_objects.append(self.object_factory())

        return Flow(workflow, states, transition_metas, transitions_approval_metas, workflow_objects)
