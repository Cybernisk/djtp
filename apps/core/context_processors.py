# coding: utf-8
from django.utils import timezone
from django.conf import settings


def global_referer(request):
    return {
        'current_referer': "http://%s%s" % (
            request.META.get("HTTP_HOST", "localhost"),
            request.META.get('PATH_INFO', '/')),
        'global_referer': request.META.get('HTTP_REFERER', '/')
    }


def global_settings(request):
    return {
        'gs': settings,
        'get_full_path': request.get_full_path(),
        'current_date': timezone.now(),
    }


def session(request):
    return {
        'session': request.session,
    }


def template(request):
    return {
        'base': settings.DEFAULT_TEMPLATE
    }
