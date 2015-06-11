"""Helpers.

.. module:: core.helpers
   :platform: Linux, Unix
   :synopsis: Lesser helpers for routing operations
.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""
# coding: utf-8
import six
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
from functools import reduce


# safe method get obj.attr.attr1 and so on
# safe_ret(cell, 'room.pk')
# safe_ret(cell, 'room.base.pk')
safe_ret = (
    lambda x, y: reduce(
        lambda el, attr: (
            getattr(el, attr)() if callable(getattr(el, attr))
            else getattr(el, attr)
        )
        if hasattr(el, attr) else None,
        [x, ] + y.split('.')
    )
)

get_int_or_zero = lambda x: int(x) if (
    x.isdigit() if isinstance(x, six.string_types) else x
) else 0


# noinspection PyProtectedMember,PyUnresolvedReferences
def get_content_type(obj):
    """
    Gets content_type for ``Object``.
    Works with ModelBase based classes, its instances
    and with format string ``'app_label.model_name'``, also supports
    django-sphinx models and instances modification
    retrieves content_type or raise the common django Exception

    :returns: ``ContentType`` instance
    :param obj: Model class, instance, basestring classpath instance
    :type obj: django.db.models.Model or str
    :exception: ObjectDoestNotExist, MultipleObjectsReturned

    .. code-block:: python

        user_content_type = get_content_type(User)
        user_content_type = get_content_type(onsite_user)
        user_content_type = get_content_type('auth.user')
    """
    app_label, model = '-1', '-1'
    if callable(obj):  # class
        model = obj._meta.model_name
        app_label = obj._meta.app_label
    elif hasattr(obj, 'pk'):  # class instance
        app_label = obj._meta.app_label
        model = obj._meta.model_name
    elif isinstance(obj, six.string_types):
        app_label, model = obj.split('.')
    ct = ContentType.objects.get(app_label=app_label, model=model)
    return ct


# noinspection PyPep8Naming
def get_content_type_or_None(source):
    """Gets ``source`` content_type or returns None

    :returns: ``ContentType`` instance or None
    """
    try:
        return get_content_type(source)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return None


def get_content_type_or_404(source):
    """Gets ``source`` content_type or raises Http404

    :returns: ``ContentType`` instance
    :exception: Http404
    """
    try:
        return get_content_type(source)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        raise Http404
