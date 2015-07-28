from river.handlers.handler import Handler
from river.signals import workflow_is_completed_successfully

__author__ = 'ahmetdal'


class CompletedSuccessfullyHandler(Handler):
    handlers = []

    @classmethod
    def dispatch(cls, sender, workflow_object, field, *args, **kwargs):
        suitable_handlers = filter(
            lambda h:
            h.get('workflow_object_pk', workflow_object.pk) == workflow_object.pk and
            h.get('field', field) == field, CompletedSuccessfullyHandler.handlers
        )

        for handler in suitable_handlers:
            handler.get('handler')(object=workflow_object, field=field)

    @classmethod
    def register(cls, *args, **kwargs):
        d = super(CompletedSuccessfullyHandler, cls).register(*args, **kwargs)
        CompletedSuccessfullyHandler.handlers.append(d)


workflow_is_completed_successfully.connect(CompletedSuccessfullyHandler.dispatch)
