from hamcrest import all_of, has_property
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher


def has_permission(name, match):
    return HasPermissions(name, wrap_matcher(match))


def has_transition(source_state, destination_state, iteration=None):
    return HasTransition(source_state, destination_state, iteration=iteration)


class HasPermissions(BaseMatcher):
    def __init__(self, permission_property_name, value_matcher):
        self.permission_property_name = permission_property_name
        self.value_matcher = value_matcher

    def describe_to(self, description):
        description.append_text("an object with a permission'") \
            .append_text(self.permission_property_name) \
            .append_text("' matching ") \
            .append_description_of(self.value_matcher)

    def _matches(self, item):
        if item is None:
            return False

        if not hasattr(item, self.permission_property_name):
            return False

        permission_field = getattr(item, self.permission_property_name)
        return self.value_matcher.matches(permission_field.all())


class HasTransition(BaseMatcher):
    def __init__(self, source_state, destination_state, iteration=None):
        self.source_state = source_state
        self.destination_state = destination_state
        self.iteration = iteration

        conditions = [
            has_property("source_state", source_state),
            has_property("destination_state", destination_state)
        ]
        if iteration:
            conditions.append(has_property("iteration", iteration))

        self.value_matcher = all_of(*conditions)

    def describe_to(self, description):
        description.append_text("an object with a transition (%s -> %s) (%s)'" % (self.source_state, self.destination_state, self.iteration)) \
            .append_text("' matching ") \
            .append_description_of(self.value_matcher)

    def _matches(self, item):
        if item is None:
            return False

        return self.value_matcher.matches(getattr(item, "transition"))
