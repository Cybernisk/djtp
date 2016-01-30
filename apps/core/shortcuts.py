"""Shortcuts

.. module:: core.shortcuts
   :platform: Linux, Unix
   :synopsis: Shortcuts for core app
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibrary.ru>

"""
# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


def direct_to_template(request, template, context=None, processors=None):
    """return response object

    :param request: Django ``HttpRequest`` instance
    :param template: template file place on filesystem and stored in
        template directory ex. ``'accounts/profile.html'``
    :param context: ``dict`` instance with render context

        .. code-block:: python

            {'context': True, 'time': datetime.now()}

    :param processors: context processors
    :returns: ``HttpResponse`` object instance
    """
    context = context or {}
    processors = processors or []
    return render_to_response(
        template, context,
        context_instance=RequestContext(request, processors=processors))
