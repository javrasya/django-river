from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed

from river.models.proceeding import Proceeding
from river.models.proceeding_meta import ProceedingMeta, post_group_change, post_permissions_change
from river.services.proceeding_meta import ProceedingMetaService
from river.tests.base_test import BaseTestCase
from river.tests.models import TestModel
from river.tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


class test_ProceedingMetaService(BaseTestCase):
    def setUp(self):
        from river.models.factories import ProceedingMetaObjectFactory, StateObjectFactory

        self.state1 = StateObjectFactory()
        self.state2 = StateObjectFactory()
        self.state3 = StateObjectFactory()
        self.content_type = ContentType.objects.get_for_model(TestModel)

        self.proceeding_meta = ProceedingMetaObjectFactory(content_type=self.content_type, transition__source_state=self.state1, transition__destination_state=self.state2)
        self.object = TestModelObjectFactory().model
        self.field = "my_field"

    def test_apply_new_proceed_definition(self):
        from river.models.factories import ProceedingMetaObjectFactory, TransitionObjectFactory

        ct = self.proceeding_meta.content_type
        # self.assertEqual(0, Proceeding.objects.filter(workflow_object=self.object).count())
        # ObjectService.register_object(self.object, self.field)
        self.assertEqual(1, Proceeding.objects.filter(workflow_object=self.object).count())

        transition = TransitionObjectFactory(source_state=self.state2, destination_state=self.state3)

        m2m_changed.disconnect(post_group_change, ProceedingMeta.groups.through)
        m2m_changed.disconnect(post_permissions_change, ProceedingMeta.permissions.through)

        proceeding_meta = ProceedingMetaObjectFactory(content_type=ct, field=self.field, transition=transition, permissions__in=self.proceeding_meta.permissions.all())

        self.assertEqual(1, Proceeding.objects.filter(workflow_object=self.object, field=self.field).count())

        ProceedingMetaService.apply_new_proceeding_meta(proceeding_meta)

        self.assertEqual(2, Proceeding.objects.filter(workflow_object=self.object, field=self.field).count())

        proceeding_meta.save()

        self.assertEqual(2, Proceeding.objects.filter(workflow_object=self.object, field=self.field).count())
