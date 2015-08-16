from django.dispatch import Signal

__author__ = 'ahmetdal'

pre_final = Signal(providing_args=["workflow_object", "field"])
post_final = Signal(providing_args=["workflow_object", "field"])

pre_transition = Signal(providing_args=["workflow_object", "field", "source_state", "destination_state", "approvement"])
post_transition = Signal(providing_args=["workflow_object", "field", "source_state", "destination_state", "approvement"])

pre_approved = Signal(providing_args=["workflow_object", "field", "approvement", "track"])
post_approved = Signal(providing_args=["workflow_object", "field", "approvement", "track"])


class TransitionSignal(object):
    def __init__(self, status, workflow_object, field, approvement):
        self.status = status
        self.workflow_object = workflow_object
        self.field = field
        self.approvement = approvement

    def __enter__(self):
        if self.status:
            pre_transition.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                field=self.field,
                source_state=self.approvement.meta.transition.source_state,
                destination_state=self.approvement.meta.transition.destination_state,
                approvement=self.approvement,
            )

    def __exit__(self, type, value, traceback):
        if self.status:
            post_transition.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                field=self.field,
                source_state=self.approvement.meta.transition.source_state,
                destination_state=self.approvement.meta.transition.destination_state,
                approvement=self.approvement,
            )


class ApprovementSignal(object):
    def __init__(self, workflow_object, field, approvement, track):
        self.workflow_object = workflow_object
        self.field = field
        self.approvement = approvement
        self.track = track

    def __enter__(self):
        pre_approved.send(
            sender=ApprovementSignal.__class__,
            workflow_object=self.workflow_object,
            field=self.field,
            approvement=self.approvement,
            track=self.track
        )

    def __exit__(self, type, value, traceback):
        post_approved.send(
            sender=TransitionSignal.__class__,
            workflow_object=self.workflow_object,
            field=self.field,
            approvement=self.approvement,
            track=self.track
        )


class FinalSignal(object):
    def __init__(self, workflow_object, field):
        self.workflow_object = workflow_object
        self.field = field
        self.status = self.workflow_object.on_final_state

    def __enter__(self):
        if self.status:
            pre_final.send(
                sender=FinalSignal.__class__,
                workflow_object=self.workflow_object,
                field=self.field
            )

    def __exit__(self, type, value, traceback):
        if self.status:
            post_final.send(
                sender=TransitionSignal.__class__,
                workflow_object=self.workflow_object,
                field=self.field,
            )
