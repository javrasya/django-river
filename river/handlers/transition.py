from river.handlers.handler import Handler
from river.signals import on_transition

__author__ = 'ahmetdal'


class TransitionHandler(Handler):
    handlers = []

    @classmethod
    def dispatch(cls, sender, workflow_object, field, source_state, destination_state, *args, **kwargs):
        suitable_handlers = filter(
            lambda h:
            h.get('workflow_object_pk', workflow_object.pk) == workflow_object.pk and
            h.get('field', field) == field and
            h.get('source_state_pk', source_state.pk) == source_state.pk and
            h.get('destination_state_pk', destination_state.pk) == destination_state.pk, TransitionHandler.handlers
        )

        for handler in suitable_handlers:
            handler.get('handler')(object=workflow_object, field=field, source_state=source_state, destination_state=destination_state)

    @classmethod
    def register(cls, handler, source_state=None, destination_state=None, *args, **kwargs):

        d = super(TransitionHandler, cls).register(handler, *args, **kwargs)
        if source_state:
            d['source_state_pk'] = source_state.pk
        if destination_state:
            d['destination_state_pk'] = destination_state.pk
        TransitionHandler.handlers.append(d)


on_transition.connect(TransitionHandler.dispatch)
