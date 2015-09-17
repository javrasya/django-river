from river.tests.models import TestModel

__author__ = 'ahmetdal'


class TestModelObjectFactory():
    def __init__(self):
        self.model = TestModel.objects.create(test_field="")

    @staticmethod
    def create_batch(size):
        for i in range(size):
            TestModel.objects.create(test_field=i)
        return TestModel.objects.all()
