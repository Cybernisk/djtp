"""Decorators

.. module:: core.decorators
   :platform: Linux, Unix
   :synopsis: core decorators

.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""
# coding: utf-8
from django.http import HttpResponse
from functools import wraps


def login_required_json(func):
    """login_required_json decorator, returns HttpResponse with
    ``content_type='application/json'`` object

    :returns: ``HttpResponse`` with ``'application/json'`` content_type.
    Sets ``{"success": False}`` if user is not logged in
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
        response.write('{"success": false, "error": "login requried"}')
        return response
    return wrapper
