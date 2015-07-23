# -*- coding: utf-8 -*-
# #----------------------------------------------------------------------
# # WEB Middleware Classes


# # Python modules
import logging

from django.conf import settings


try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
# # Django modules



# #
# # Thread local storage
# #
_tls = local()

logger = logging.getLogger(__name__)


class TLSMiddleware(object):
    """
    Thread local storage middleware
    """

    def process_request(self, request):
        from apps.riverio.models.application import Application

        """
        Set up TLS' user and request
        """
        _tls.request = request
        if settings.TOKEN_KEY in request.META:
            wa2s_token = request.META[settings.TOKEN_KEY]
            try:
                application = Application.objects.get(applicationtoken=wa2s_token)
                set_application(application)
                request.application = application
            except Application.DoesNotExist:
                logging.debug("There is not application with the token %s" % wa2s_token)


    def process_response(self, request, response):
        """
        Clean TLS
        """
        _tls.request = None
        _tls.application = None
        return response

    def process_exception(self, request, exception):
        """
        Clean TLS
        """
        _tls.request = None
        _tls.application = None


def set_application(application):
    """
    Set up TLS user
    """
    _tls.application = application


def get_application():
    """
    Get current TLS user
    """
    return getattr(_tls, "application", None)


def get_request():
    """
    Get current TLS request
    """
    return getattr(_tls, "request", None)
