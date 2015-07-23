import factory

from tests.apps.riverio.base_test import BaseTestCase
from tests.models import TestModel

from tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


class ApprovementServiceBasedTest(BaseTestCase):
    def setUp(self):
        from apps.riverio.models.factories import \
            FieldObjectFactory, \
            TransitionObjectFactory, \
            ExternalUserObjectFactory, \
            ExternalPermissionObjectFactory, \
            ExternalContentTypeObjectFactory, \
            ApprovementMetaObjectFactory, \
            StateObjectFactory, \
            ApplicationObjectFactory

        TransitionObjectFactory.reset_sequence(0)
        ApprovementMetaObjectFactory.reset_sequence(0)
        StateObjectFactory.reset_sequence(0)
        TestModel.objects.all().delete()

        self.application = ApplicationObjectFactory()
        self.content_type = ExternalContentTypeObjectFactory(application=self.application)
        self.permissions = ExternalPermissionObjectFactory.create_batch(4, application=self.application, content_type=self.content_type)
        self.user1 = ExternalUserObjectFactory(application=self.application, permissions=[self.permissions[0]])
        self.user2 = ExternalUserObjectFactory(application=self.application, permissions=[self.permissions[1]])
        self.user3 = ExternalUserObjectFactory(application=self.application, permissions=[self.permissions[2]])
        self.user4 = ExternalUserObjectFactory(application=self.application, permissions=[self.permissions[3]])

        self.field = FieldObjectFactory(application=self.application)
        self.states = StateObjectFactory.create_batch(
            9,
            application=self.application,
            label=factory.Sequence(lambda n: "s%s" % str(n + 1) if n <= 4 else ("s4.%s" % str(n - 4) if n <= 6 else "s5.%s" % str(n - 6)))
        )
        self.transitions = TransitionObjectFactory.create_batch(8,
                                                                content_type=self.content_type,
                                                                field=self.field,
                                                                source_state=factory.Sequence(
                                                                    lambda n: self.states[n] if n <= 2 else (self.states[n - 1]) if n <= 4 else (self.states[n - 2] if n <= 6 else self.states[4])),
                                                                destination_state=factory.Sequence(lambda n: self.states[n + 1]))

        self.approvement_metas = ApprovementMetaObjectFactory.create_batch(
            9,
            transition=factory.Sequence(lambda n: self.transitions[n] if n <= 1 else self.transitions[n - 1]),
            order=factory.Sequence(lambda n: 1 if n == 2 else 0)
        )

        for n, approvement_meta in enumerate(self.approvement_metas):
            approvement_meta.permission.add(self.permissions[n] if n <= 3 else self.permissions[3])
            approvement_meta.save()

        self.objects = TestModelObjectFactory.create_batch(2)
