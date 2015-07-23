# Create your views here.

from esefpy.web.rest.viewsets import BaseAPIView
from rest_framework.response import Response


__author__ = 'ahmetdal'


class DataFormsViewSet(BaseAPIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'id': user.id,
        })




