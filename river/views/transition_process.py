from copy import copy
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from apps.riverio.services.transition import TransitionService
from apps.riverio.views.tokenized import TokenizedMixin
from apps.riverio.views.serializers.transition_process_serializer import TransitionProcessSerializer, APPROVE, REJECT

__author__ = 'ahmetdal'


class TransitionProcessView(APIView, TokenizedMixin):
    """
    Processing transition API for objects to APPROVE(1) or REJECT(0) transitions.
    """

    def get_serializer_class(self, *args, **kwargs):
        return TransitionProcessSerializer

    def post(self, request, format=None):
        serializer = TransitionProcessSerializer(data=request.DATA)
        if serializer.is_valid():
            data = copy(serializer.data)
            process_type = data.pop('process_type')
            if process_type == APPROVE:
                TransitionService.approve_transition(**data)
            elif process_type == REJECT:
                TransitionService.reject_transition(**data)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)