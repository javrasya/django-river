from esefpy.web.rest.viewsets import BaseAPIView
from rest_framework.response import Response

from apps.riverio.services.approvement import ApprovementService
from apps.riverio.views.tokenized import TokenizedMixin


__author__ = 'ahmetdal'


class IsUserAuthorizedView(BaseAPIView, TokenizedMixin):
    """
        View to check user has any role for a content type and field. If there is any approvements waiting for approval currently, approved or rejected
        in pasts means user is authorized.
    """

    def get(self, request, content_type_id, field_id, user_id):
        return Response({
            'is_authorized': ApprovementService.has_user_any_action(content_type_id, field_id, user_id)
        })
