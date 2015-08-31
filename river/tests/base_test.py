from django.test import TestCase

__author__ = 'ahmetdal'


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        print('%s is initialized' % self.__class__)

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        print('%s is finished' % self.__class__)
