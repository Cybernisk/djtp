"""Forms

.. module:: core.forms
   :platform: Linux, Unix
   :synopsis: core forms classes and mixins

.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""
# coding: utf-8
from django import forms


class RequestModelForm(forms.ModelForm):
    """ RequestModelForm, bases on ``forms.ModelForm`` class
    use RequestFormMixin instead of it
    """
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        super(RequestModelForm, self).__init__(*args, **kwargs)


class RequestFormMixin(object):
    """RequestFormMixin, store Django ``request`` instance in self.request

    .. note::

        ``request`` instance should be given via keywords while
        form instance init

    .. code-block:: python

        class RequestForm(RequestFormMixin, forms.ModelForm):
            class Meta:
                model = SomeModel

        def foo(request):
            form = RequestForm(request.POST or None, request=request)
            ...
    """
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        super(RequestFormMixin, self).__init__(*args, **kwargs)
