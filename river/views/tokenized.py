from apps.riverio.utils.authentication import RiverIOTokenAuthentication

__author__ = 'ahmetdal'


class TokenizedMixin(object):
    authentication_classes = (RiverIOTokenAuthentication,)