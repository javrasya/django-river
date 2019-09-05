from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, has_value, is_not, has_key, has_property, has_length, has_item

from river.config import app_config
from river.hooking.backends.loader import callback_backend
from river.hooking.transition import PostTransitionHooking
from river.models.factories import PermissionObjectFactory, StateObjectFactory, WorkflowFactory, TransitionApprovalMetaFactory
from river.tests.models import BasicTestModel
from river.tests.models.factories import BasicTestModelObjectFactory

__author__ = 'ahmetdal'


def test_callback(*args, **kwargs):
    pass


# noinspection DuplicatedCode
class MemoryHookingBackendTest(TestCase):
    def setUp(self):
        self.field_name = "my_field"
        authorized_permission = PermissionObjectFactory()

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

        app_config.HOOKING_BACKEND_CLASS = 'river.hooking.backends.memory.MemoryHookingBackend'
        self.handler_backend = callback_backend
        self.handler_backend.callbacks = {}

    def test_shouldRegisterAHooking(self):
        workflow_objects = BasicTestModelObjectFactory.create_batch(2)

        hooking_hash = '%s.%s_object%s_field_name%s' % (PostTransitionHooking.__module__, PostTransitionHooking.__name__, workflow_objects[1].pk, self.field_name)

        assert_that(self.handler_backend.callbacks, is_not(has_key(hooking_hash)))

        self.handler_backend.register(PostTransitionHooking, test_callback, workflow_objects[1], self.field_name)

        assert_that(self.handler_backend.callbacks, has_key(hooking_hash))
        assert_that(self.handler_backend.callbacks, has_value(has_property("__name__", test_callback.__name__)))

    def test_shouldReturnTheRegisteredHooking(self):
        workflow_object = BasicTestModelObjectFactory().model

        self.handler_backend.register(PostTransitionHooking, test_callback, workflow_object, self.field_name)
        callbacks = self.handler_backend.get_callbacks(PostTransitionHooking, workflow_object, self.field_name)

        assert_that(callbacks, has_length(1))
        assert_that(callbacks, has_item(has_property("__name__", test_callback.__name__)))

    def test_shouldUnregisterAHooking(self):
        workflow_objects = BasicTestModelObjectFactory.create_batch(2)

        hooking_hash = '%s.%s_object%s_field_name%s' % (PostTransitionHooking.__module__, PostTransitionHooking.__name__, workflow_objects[1].pk, self.field_name)

        assert_that(self.handler_backend.callbacks, is_not(has_key(hooking_hash)))

        self.handler_backend.register(PostTransitionHooking, test_callback, workflow_objects[1], self.field_name)

        assert_that(self.handler_backend.callbacks, has_key(hooking_hash))
        assert_that(self.handler_backend.callbacks, has_value(has_property("__name__", test_callback.__name__)))

        self.handler_backend.unregister(PostTransitionHooking, workflow_objects[1], self.field_name)

        assert_that(self.handler_backend.callbacks, is_not(has_key(hooking_hash)))
        assert_that(self.handler_backend.callbacks, is_not(has_value(has_property("__name__", test_callback.__name__))))

    def test_shouldRemoveTheHookingWhenWorkflowObjectIsDeleted(self):
        workflow_object = BasicTestModelObjectFactory().model

        hooking_hash = '%s.%s_object%s_field_name%s' % (PostTransitionHooking.__module__, PostTransitionHooking.__name__, workflow_object.pk, self.field_name)

        assert_that(self.handler_backend.callbacks, is_not(has_key(hooking_hash)))
        assert_that(self.handler_backend.callbacks, is_not(has_value(has_property("__name__", test_callback.__name__))))

        self.handler_backend.register(PostTransitionHooking, test_callback, workflow_object, self.field_name)

        assert_that(self.handler_backend.callbacks, has_key(hooking_hash))
        assert_that(self.handler_backend.callbacks, has_value(has_property("__name__", test_callback.__name__)))

        workflow_object.delete()

        assert_that(self.handler_backend.callbacks, is_not(has_key(hooking_hash)))
        assert_that(self.handler_backend.callbacks, is_not(has_value(has_property("__name__", test_callback.__name__))))
