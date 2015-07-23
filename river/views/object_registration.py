from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from apps.riverio.services.object import ObjectService
from apps.riverio.views.tokenized import TokenizedMixin
from apps.riverio.views.serializers.object_registration_serializer import ObjectRegistrationSerializer

__author__ = 'ahmetdal'


class ObjectRegistrationView(APIView, TokenizedMixin):
    """
     API to register objects
    """

    serializer = ObjectRegistrationSerializer

    def post(self, request, format=None):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            ObjectService.register_object(**serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)