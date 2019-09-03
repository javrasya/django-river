from river.tests.models import BasicTestModel

__author__ = 'ahmetdal'


class BasicTestModelObjectFactory(object):
    def __init__(self):
        self.model = BasicTestModel.objects.create(test_field="")

    @staticmethod
    def create_batch(size):
        for i in range(size):
            BasicTestModel.objects.create(test_field=i)
        return BasicTestModel.objects.all()
