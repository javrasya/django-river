from river.handlers.handler import Handler
from river.signals import pre_transition, post_transition

__author__ = 'ahmetdal'


class TransitionHandler(Handler):
    @classmethod
    def get_hash(cls, workflow_object, field, source_state=None, destination_state=None, proceeding=None, *args, **kwargs):
        return super(TransitionHandler, cls).get_hash(workflow_object, field) + ('source_state' + str(source_state.pk) if source_state else '') + (
            'destination_state' + str(destination_state.pk) if destination_state else '') + ('proceeding' + str(proceeding.pk) if proceeding else '')


class PreTransitionHandler(TransitionHandler):
    pass


class PostTransitionHandler(TransitionHandler):
    pass


pre_transition.connect(PreTransitionHandler.dispatch)
post_transition.connect(PostTransitionHandler.dispatch)
