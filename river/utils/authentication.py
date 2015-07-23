from django.conf import settings
from esefpy.common.django.middlewares.tls import set_user

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from apps.riverio.models.application_token import ApplicationToken


__author__ = 'ahmetdal'


class RiverIOTokenAuthentication(TokenAuthentication):
    model = ApplicationToken


    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if len(auth) == 2 and auth[0].lower() == b'token':
            auth = auth[1:]
        if not auth:
            msg = 'No River.IO token is provided. Please send your token in %s as your request parameter' % settings.TOKEN_KEY
            raise exceptions.NotAuthenticated(msg)

        if len(auth) > 1:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        user, token = self.authenticate_credentials(auth[0])
        set_user(user)
        return user, token


    def authenticate_header(self, request):
        return None