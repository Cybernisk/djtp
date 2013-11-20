"""Context processors

.. module:: core.context_processors
   :platform: Linux, Unix
   :synopsis: core context processors

.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""
# coding: utf-8

from django.utils import timezone
from django.conf import settings


def global_referer(request):
    """global_referer context processor

    :returns: current_referer sets to current URI (HTTP_HOST + PATH_INFO)

        global_referer sets to HTTP_REFERER

    .. code-block:: django

        <input value='{{ global_referer }}' name='next' />
        {{ current_date|timezone:"Europe/London"|date:"d.m.Y H:i" }}

    """
    return {
        'current_referer': "http://%s%s" % (
            request.META.get("HTTP_HOST", "localhost"),
            request.META.get('PATH_INFO', '/')),
        'global_referer': request.META.get('HTTP_REFERER', '/')
    }


def global_settings(request):
    """global settings context processor

    :return: gs as django.conf.settings object

        get_full_path as ``request.get_full_path()`` instance

        current_date as ``timezone.now()``

    .. code-block:: django

        {% load tz i18n %}
        I18N is currently {{ gs.I18N|yesno:"enabled, disabled" }}
        {{ current_date|timezone:"Europe/London"|date:"d.m.Y H:i" }}
    """
    return {
        'gs': settings,
        'get_full_path': request.get_full_path(),
        'current_date': timezone.now(),
    }


def session(request):
    """session context processor

    :return: session as ``request.session`` instance
    """
    return {
        'session': request.session,
    }


def template(request):
    """template context processor

    :return: base as ``settings.DEFAULT_TEMPLATE``

    .. code-block:: django

        {% extends base %}
    """
    return {
        'base': settings.DEFAULT_TEMPLATE
    }
