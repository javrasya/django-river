from uuid import uuid4

from django.test import TestCase

from river.tests.models import BasicTestModel

callback_output = {

}


def callback_func(context, test_identifier):
    print(context)
    callback_output[test_identifier] = callback_output.get(test_identifier, []) + [context]


class BaseStaticHookingTest(TestCase):

    def setUp(self):
        self.identifier = str(uuid4())
        self.callback_function = lambda context: callback_func(context, self.identifier)

    def get_output(self):
        return callback_output.get(self.identifier, None)

    def hook_pre_approve(self, transition_approval_meta, workflow_object=None, transition_approval=None):
        river_object = workflow_object.river.my_field if workflow_object else BasicTestModel.river.my_field
        river_object.on_pre_approve(self.callback_function, transition_approval_meta, transition_approval=transition_approval)

    def hook_pre_transition(self, transition_meta, workflow_object=None, transition=None):
        river_object = workflow_object.river.my_field if workflow_object else BasicTestModel.river.my_field
        river_object.on_pre_transition(self.callback_function, transition_meta, transition=transition)

    def hook_post_transition(self, transition_meta, workflow_object=None, transition=None):
        river_object = workflow_object.river.my_field if workflow_object else BasicTestModel.river.my_field
        river_object.on_post_transition(self.callback_function, transition_meta, transition=transition)

    def hook_pre_complete(self, workflow_object=None):
        river_object = workflow_object.river.my_field if workflow_object else BasicTestModel.river.my_field
        river_object.on_pre_complete(self.callback_function)

    def hook_post_complete(self, workflow_object=None):
        river_object = workflow_object.river.my_field if workflow_object else BasicTestModel.river.my_field
        river_object.on_post_complete(self.callback_function)
