from django.test import TestCase
from river.models.state import State

__author__ = 'ahmetdal'


class test__StateModel(TestCase):
    def test_on_pre_save_without_slug(self):
        expected_slug = 'test-label'
        state = State(label='Test Label')
        state.save()
        self.assertEqual(expected_slug, state.slug)

    def test_on_pre_save_with_wrong_formatted_slug(self):
        expected_slug = 'test-slug'
        state = State(label='Test Label', slug='Test Slug')
        state.save()
        self.assertEqual(expected_slug, state.slug)
