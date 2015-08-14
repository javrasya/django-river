from river.handlers.handler import Handler
from river.signals import pre_transition, post_transition

__author__ = 'ahmetdal'


class TransitionHandler(Handler):
    handlers = {}

    @classmethod
    def get_handler(cls, handler, workflow_object, field, source_state=None, destination_state=None, approvement=None, *args, **kwargs):
        d = super(TransitionHandler, cls).get_handler(handler, workflow_object, field, *args, **kwargs)
        if source_state:
            d['source_state_pk'] = source_state.pk
        if destination_state:
            d['destination_state_pk'] = destination_state.pk
        return d

    @classmethod
    def get_hash(cls, workflow_object, field, source_state=None, destination_state=None, approvement=None, *args, **kwargs):
        return super(TransitionHandler, cls).get_hash(workflow_object, field) + ('source_state' + str(source_state.pk) if source_state else '') + (
            'destination_state' + str(destination_state.pk) if destination_state else '') + ('approvement' + str(approvement.pk) if approvement else '')


class PreTransitionHandler(TransitionHandler):
    handlers = {}


class PostTransitionHandler(TransitionHandler):
    handlers = {}


pre_transition.connect(PreTransitionHandler.dispatch)
post_transition.connect(PostTransitionHandler.dispatch)
