from behave import given, when

from features.steps.basic_steps import workflow_object


@given('a bug "{description:ws}" identifier "{identifier:ws}"')
def issue(context, description, identifier):
    workflow_object(context, identifier)


def _approve(context, workflow_object_identifier, username, next_state):
    from django.contrib.auth.models import User
    from river.models import State

    workflow_object = getattr(context, "workflow_objects", {})[workflow_object_identifier]

    user = User.objects.get(username=username)
    workflow_object.river.my_field.approve(as_user=user, next_state=State.objects.get(label=next_state))


@when('"{workflow_object_identifier:ws}" is attempted to be closed by {username:w}')
def close_issue(context, workflow_object_identifier, username):
    _approve(context, workflow_object_identifier, username, "Closed")


@when('"{workflow_object_identifier:ws}" is attempted to be re-opened by {username:w}')
def re_open_issue(context, workflow_object_identifier, username):
    _approve(context, workflow_object_identifier, username, "Re-Opened")
