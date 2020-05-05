from river.tests.models import BasicTestModel, ModelWithTwoStateFields


class BasicTestModelObjectFactory(object):
    def __init__(self, workflow):
        self.model = BasicTestModel.objects.create(test_field="", workflow=workflow)

    @staticmethod
    def create_batch(size, workflow):
        for i in range(size):
            BasicTestModel.objects.create(test_field=i, workflow=workflow)
        return BasicTestModel.objects.all()


class ModelWithTwoStateFieldsObjectFactory(object):
    def __init__(self, workflow):
        self.model = ModelWithTwoStateFields.objects.create(workflow=workflow)

    @staticmethod
    def create_batch(size):
        for i in range(size):
            ModelWithTwoStateFields.objects.create()
        return ModelWithTwoStateFields.objects.all()
