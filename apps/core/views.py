"""Views

.. module:: core.views
   :platform: Linux, Unix
   :synopsis: core class based views and mixins

.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""
# -*- coding: utf-8 -*-

from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class IndexView(generic.TemplateView):
    """Index view"""
    template_name = 'index.html'


class LoginRequiredMixin(object):
    """LoginRequired View Mixin"""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)
