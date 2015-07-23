from rest_framework.response import Response
from rest_framework.views import APIView
from apps.riverio.services.object import ObjectService
from apps.riverio.views.tokenized import TokenizedMixin

__author__ = 'ahmetdal'


class ObjectCountWaitingForApprovalView(APIView, TokenizedMixin):
    """
    An API that returns the count of object waiting for approval.
    """

    def get(self, request, content_type_id, field_id, user_id):
        return Response(
            {'count': ObjectService.get_object_count_waiting_for_approval(content_type_id, field_id, user_id)}
        )