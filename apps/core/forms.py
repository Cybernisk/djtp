# coding: utf-8
from django import forms


class RequestModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        super(RequestModelForm, self).__init__(*args, **kwargs)


class RequestFormMixin(object):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        super(RequestFormMixin, self).__init__(*args, **kwargs)