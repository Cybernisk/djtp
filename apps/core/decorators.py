# coding: utf-8
from django.http import HttpResponse


def login_required_json(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
        response.write('{"success": false, "error": "login requried"}')
        return response
    return wrapper
