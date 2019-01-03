from river.hooking.hooking import Hooking
from river.signals import pre_transition, post_transition

__author__ = 'ahmetdal'


class TransitionHooking(Hooking):

    @staticmethod
    def get_result_exclusions():
        return ["source_state", "destination_state"]

    @classmethod
    def get_hash(cls, workflow_object, field_name, source_state=None, destination_state=None, transition_approval=None, *args, **kwargs):
        return super(TransitionHooking, cls).get_hash(workflow_object, field_name) + ('source_state' + str(source_state.pk) if source_state else '') + (
            'destination_state' + str(destination_state.pk) if destination_state else '') + ('transition_approval' + str(transition_approval.pk) if transition_approval else '')


class PreTransitionHooking(TransitionHooking):
    pass


class PostTransitionHooking(TransitionHooking):
    pass


pre_transition.connect(PreTransitionHooking.dispatch)
post_transition.connect(PostTransitionHooking.dispatch)
