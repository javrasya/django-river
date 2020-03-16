import factory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from factory import DjangoModelFactory

from river.models import Workflow, TransitionMeta
from river.models.state import State
from river.models.transitionapprovalmeta import TransitionApprovalMeta


class ContentTypeObjectFactory(DjangoModelFactory):
    class Meta:
        model = ContentType

    model = factory.Sequence(lambda n: 'ect_model_%s' % n)


class UserObjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'User_%s' % n)

    @factory.post_generation
    def user_permissions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for permission in extracted:
                self.user_permissions.add(permission)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


class GroupObjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'auth.Group'

    name = factory.Sequence(lambda n: 'Group_%s' % n)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for permission in extracted:
                self.permissions.add(permission)


class PermissionObjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'auth.Permission'

    name = factory.Sequence(lambda n: 'Permission_%s' % n)
    codename = factory.Sequence(lambda n: 'Codename_%s' % n)
    content_type = factory.SubFactory(ContentTypeObjectFactory)


class StateObjectFactory(DjangoModelFactory):
    class Meta:
        model = State

    label = factory.Sequence(lambda n: 's%s' % n)
    description = factory.Sequence(lambda n: 'desc_%s' % n)


class WorkflowFactory(DjangoModelFactory):
    class Meta:
        model = Workflow

    content_type = factory.SubFactory(ContentTypeObjectFactory)
    initial_state = factory.SubFactory(StateObjectFactory)


class TransitionMetaFactory(DjangoModelFactory):
    class Meta:
        model = TransitionMeta

    source_state = factory.SubFactory(StateObjectFactory)
    destination_state = factory.SubFactory(StateObjectFactory)
    workflow = factory.SubFactory(WorkflowFactory)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for permission in extracted:
                self.permissions.add(permission)


class TransitionApprovalMetaFactory(DjangoModelFactory):
    class Meta:
        model = TransitionApprovalMeta

    transition_meta = factory.SubFactory(TransitionMetaFactory)
    workflow = factory.SubFactory(WorkflowFactory)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for permission in extracted:
                self.permissions.add(permission)
