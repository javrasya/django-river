from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden
from apps.riverio.models import Application


__author__ = 'ahmetdal'


def login_with_wa2s_token_is_required(func=None):
    @wraps(func)
    def decorated(request, *args, **kwargs):
        if settings.TOKEN_KEY in request.META:
            wa2s_token = request.META[settings.TOKEN_KEY]

            try:
                Application.objects.get(token=wa2s_token)
                return func(request, *args, **kwargs)
            except Application.DoesNotExist:
                return HttpResponseForbidden()

        else:
            return HttpResponseForbidden()

    return decorated