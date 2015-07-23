from functools import wraps
import json

from django.db.models import QuerySet
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from apps.riverio.models import BaseModel


__author__ = 'ahmetdal'


def wa2s_restful(func=None):
    @wraps(func)
    def decorated(request, *args, **kwargs):
        output = {}
        try:
            result = func(request, *args, **kwargs)
            if result:
                key = 'result'
                if isinstance(result, tuple):
                    key, result = result
                if isinstance(result, dict):
                    for k, value in result.iteritems():
                        if isinstance(value, QuerySet):
                            result[k] = list([o.detail() for o in value])
                        if isinstance(value, BaseModel):
                            result[k] = value.detail()
                    output.update(result)
                elif isinstance(result, BaseModel):
                    output[result.__class__._meta.module_name] = result.details()
                elif isinstance(result, QuerySet):
                    output[result.model._meta.module_name] = list([o.details() for o in result])
                else:
                    output[key] = result
            return HttpResponse(json.dumps(output), content_type='application/json')
        except Exception, e:
            output['error_code'] = None
            output['error_message'] = e.message
            return HttpResponseBadRequest(json.dumps(output), content_type='application/json')

    return decorated



