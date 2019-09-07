from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher


def has_permission(name, match):
    return HasPermissions(name, wrap_matcher(match))


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
