from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from river.models import Approvement
from river.models.approvement_meta import ApprovementMeta
from river.services.approvement_meta import ApprovementMetaService
from river.services.object import ObjectService
from river.signals.models.approvement_meta import on_post_save
from river.tests.base_test import BaseTestCase
from river.tests.models import TestModel
from river.tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


class test_ApprovementMetaService(BaseTestCase):
    def setUp(self):
        from river.models.factories import ApprovementMetaObjectFactory, StateObjectFactory

        self.state1 = StateObjectFactory()
        self.state2 = StateObjectFactory()
        self.state3 = StateObjectFactory()
        self.content_type = ContentType.objects.get_for_model(TestModel)

        self.approvement_meta = ApprovementMetaObjectFactory(transition__content_type=self.content_type, transition__source_state=self.state1, transition__destination_state=self.state2)
        self.object = TestModelObjectFactory().model
        self.field = "my_field"

    def test_apply_new_approve_definition(self):
        from river.models.factories import ApprovementMetaObjectFactory, TransitionObjectFactory

        ct = self.approvement_meta.transition.content_type
        self.assertEqual(0, Approvement.objects.filter(object=self.object).count())
        ObjectService.register_object(self.object, self.field)
        self.assertEqual(1, Approvement.objects.filter(object=self.object).count())

        transition = TransitionObjectFactory(content_type=ct, field=self.field, source_state=self.state2, destination_state=self.state3)

        post_save.disconnect(on_post_save, ApprovementMeta)
        approvement_meta = ApprovementMetaObjectFactory(transition=transition, permissions__in=self.approvement_meta.permissions.all())

        self.assertEqual(1, Approvement.objects.filter(object=self.object, field=self.field).count())

        ApprovementMetaService.apply_new_approvement_meta(approvement_meta)

        self.assertEqual(2, Approvement.objects.filter(object=self.object, field=self.field).count())

        approvement_meta.save()

        self.assertEqual(2, Approvement.objects.filter(object=self.object, field=self.field).count())
