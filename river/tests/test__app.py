from django.contrib import admin
from django.test import TestCase
from hamcrest import assert_that, is_not, has_item, instance_of

from river.admin import OnApprovedHookInline, OnTransitHookInline, OnCompleteHookInline, DefaultWorkflowModelAdmin
from river.models import Function
from river.tests.admin import BasicTestModelAdmin
from river.tests.models import BasicTestModel, BasicTestModelWithoutAdmin


class AppTest(TestCase):

    def test__shouldInjectExistingAdminOfTheModelThatHasStateFieldInIt(self):
        assert_that(admin.site._registry[BasicTestModel], instance_of(BasicTestModelAdmin))
        assert_that(admin.site._registry[BasicTestModel].inlines, has_item(OnApprovedHookInline))
        assert_that(admin.site._registry[BasicTestModel].inlines, has_item(OnTransitHookInline))
        assert_that(admin.site._registry[BasicTestModel].inlines, has_item(OnCompleteHookInline))

    def test__shouldInjectADefaultAdminWithTheHooks(self):
        assert_that(admin.site._registry[BasicTestModelWithoutAdmin], instance_of(DefaultWorkflowModelAdmin))
        assert_that(admin.site._registry[BasicTestModel].inlines, has_item(OnApprovedHookInline))
        assert_that(admin.site._registry[BasicTestModel].inlines, has_item(OnTransitHookInline))
        assert_that(admin.site._registry[BasicTestModel].inlines, has_item(OnCompleteHookInline))

    def test__shouldNotInjectToAdminOfTheModelThatDoesNotHaveStateFieldInIt(self):
        assert_that(admin.site._registry[Function].inlines, is_not(has_item(OnApprovedHookInline)))
        assert_that(admin.site._registry[Function].inlines, is_not(has_item(OnTransitHookInline)))
        assert_that(admin.site._registry[Function].inlines, is_not(has_item(OnCompleteHookInline)))
