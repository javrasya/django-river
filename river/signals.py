from django.dispatch import Signal

__author__ = 'ahmetdal'

workflow_is_completed = Signal(providing_args=["workflow_object", "field"])
on_transition = Signal(providing_args=["workflow_object", "field", "source_state", "destination_state"])
