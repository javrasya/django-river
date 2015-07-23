from django.core.exceptions import ObjectDoesNotExist
from esefpy.web.esefauth.backends.sf_exception_handler import sf_exception_handler
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from apps.riverio.utils.exceptions import RiverIOException


__author__ = 'ahmetdal'


def custom_exception_handler(exc):
    if isinstance(exc, ObjectDoesNotExist):
        data = {'detail': 'Not found'}
        return Response(data, status=HTTP_404_NOT_FOUND)
    if isinstance(exc, RiverIOException):
        return Response({'detail': exc.message}, status=HTTP_400_BAD_REQUEST)

    return sf_exception_handler(exc)
