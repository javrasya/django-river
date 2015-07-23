from rest_framework import viewsets

from apps.riverio.services.object import ObjectService
from apps.riverio.views.tokenized import TokenizedMixin

from apps.riverio.views.serializers.object_serializer import ObjectSerializer


__author__ = 'ahmetdal'


class ObjectsWaitingForApprovalViewSet(viewsets.ReadOnlyModelViewSet, TokenizedMixin):
    """
    An API that returns the objects waiting for approval.
    """

    serializer_class = ObjectSerializer

    def get_queryset(self):
        content_type_id = self.kwargs.get('content_type_id')
        field_id = self.kwargs.get('field_id')
        user_id = self.kwargs.get('user_id')
        return ObjectService.get_objects_waiting_for_approval(content_type_id, field_id, user_id)