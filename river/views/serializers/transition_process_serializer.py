from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


__author__ = 'ahmetdal'

REJECT = 0
APPROVE = 1

TRANSITION_PROCESS_TYPES = [
    (APPROVE, _('Approve')),
    (REJECT, _('Reject')),
]


class TransitionProcessSerializer(serializers.Serializer):
    process_type = serializers.ChoiceField(choices=TRANSITION_PROCESS_TYPES)
    content_type_id = serializers.IntegerField()
    object_id = serializers.IntegerField()
    field_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    next_state_id = serializers.IntegerField(required=False)
