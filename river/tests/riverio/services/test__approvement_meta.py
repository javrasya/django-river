from django.db.models.signals import post_save

from apps.riverio.models import Approvement
from apps.riverio.models.approvement_meta import ApprovementMeta
from apps.riverio.services.approvement_meta import ApprovementMetaService
from apps.riverio.services.object import ObjectService
from apps.riverio.signals.models.approvement_meta import on_post_save
from tests.apps.riverio.base_test import BaseTestCase
from tests.models.factories import TestModelObjectFactory

__author__ = 'ahmetdal'


class test_ApprovementMetaService(BaseTestCase):
    def setUp(self):
        from apps.riverio.models.factories import ApprovementMetaObjectFactory, StateObjectFactory, ApplicationObjectFactory

        self.application = ApplicationObjectFactory()
        self.state1 = StateObjectFactory(application=self.application)
        self.state2 = StateObjectFactory(application=self.application)
        self.state3 = StateObjectFactory(application=self.application)

        self.approvement_meta = ApprovementMetaObjectFactory(transition__source_state=self.state1, transition__destination_state=self.state2)
        self.object = TestModelObjectFactory().model

    def test_apply_new_approve_definition(self):
        from apps.riverio.models.factories import ApprovementMetaObjectFactory, TransitionObjectFactory

        ct = self.approvement_meta.transition.content_type
        field = self.approvement_meta.transition.field
        self.assertEqual(0, Approvement.objects.filter(object_id=self.object.pk, content_type=ct).count())
        ObjectService.register_object(ct.pk, self.object.pk, field.pk)
        self.assertEqual(1, Approvement.objects.filter(object_id=self.object.pk, content_type=ct).count())

        transition = TransitionObjectFactory(content_type=ct, field=field, source_state=self.state2, destination_state=self.state3)

        post_save.disconnect(on_post_save, ApprovementMeta)
        approvement_meta = ApprovementMetaObjectFactory(transition=transition, permission__in=self.approvement_meta.permission.all())

        self.assertEqual(1, Approvement.objects.filter(object_id=self.object.pk, field=field, content_type=ct).count())

        ApprovementMetaService.apply_new_approvement_meta(approvement_meta)

        self.assertEqual(2, Approvement.objects.filter(object_id=self.object.pk, field=field, content_type=ct).count())

        approvement_meta.save()

        self.assertEqual(2, Approvement.objects.filter(object_id=self.object.pk, field=field, content_type=ct).count())
