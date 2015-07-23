from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from factory import DjangoModelFactory
import factory

from river.models import Application, State, Field, Transition, ApprovementMeta

__author__ = 'ahmetdal'


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'esefauth.User'

    username = factory.Sequence(lambda n: 'User_%s' % n)


class ApplicationObjectFactory(DjangoModelFactory):
    class Meta:
        model = Application

    name = factory.Sequence(lambda n: 'app_%s' % n)
    description = factory.Sequence(lambda n: 'desc_%s' % n)
    owner = factory.SubFactory(UserFactory)


class ContentTypeObjectFactory(DjangoModelFactory):
    class Meta:
        model = ContentType

    model = factory.Sequence(lambda n: 'ect_model_%s' % n)


class PermissionObjectFactory(DjangoModelFactory):
    class Meta:
        model = Permission

    name = factory.Sequence(lambda n: 'ep_name_%s' % n)


class UserObjectFactory(DjangoModelFactory):
    class Meta:
        model = User

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for permission in extracted:
                self.permissions.add(permission)


class StateObjectFactory(DjangoModelFactory):
    class Meta:
        model = State

    label = factory.Sequence(lambda n: 's%s' % n)
    description = factory.Sequence(lambda n: 'desc_%s' % n)
    application = factory.SubFactory(ApplicationObjectFactory)


class FieldObjectFactory(DjangoModelFactory):
    class Meta:
        model = Field

    label = factory.Sequence(lambda n: 'l%s' % n)
    description = factory.Sequence(lambda n: 'desc_%s' % n)
    application = factory.SubFactory(ApplicationObjectFactory)


class TransitionObjectFactory(DjangoModelFactory):
    class Meta:
        model = Transition

    content_type = factory.SubFactory(ContentTypeObjectFactory)
    field = factory.SubFactory(FieldObjectFactory)
    source_state = factory.SubFactory(StateObjectFactory)
    destination_state = factory.SubFactory(StateObjectFactory)


class ApprovementMetaObjectFactory(DjangoModelFactory):
    class Meta:
        model = ApprovementMeta

    transition = factory.SubFactory(TransitionObjectFactory)

    @factory.post_generation
    def permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for permission in extracted:
                self.permission.add(permission)
