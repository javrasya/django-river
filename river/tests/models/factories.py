from river.tests.models import TestModel

__author__ = 'ahmetdal'


class TestModelObjectFactory():
    def __init__(self):
        self.model = TestModel.objects.create(test_field="")

    @staticmethod
    def create_batch(size):
        TestModel.objects.bulk_create(list(TestModel(test_field=str(i)) for i in range(size)))
        return TestModel.objects.all()
