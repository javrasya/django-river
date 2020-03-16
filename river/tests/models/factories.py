from river.tests.models import BasicTestModel, ModelWithTwoStateFields


class BasicTestModelObjectFactory(object):
    def __init__(self):
        self.model = BasicTestModel.objects.create(test_field="")

    @staticmethod
    def create_batch(size):
        for i in range(size):
            BasicTestModel.objects.create(test_field=i)
        return BasicTestModel.objects.all()


class ModelWithTwoStateFieldsObjectFactory(object):
    def __init__(self):
        self.model = ModelWithTwoStateFields.objects.create()

    @staticmethod
    def create_batch(size):
        for i in range(size):
            ModelWithTwoStateFields.objects.create()
        return ModelWithTwoStateFields.objects.all()
