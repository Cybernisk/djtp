"""Views

.. module:: core.views
   :platform: Linux, Unix
   :synopsis: core class based views and mixins

.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""
# coding: utf-8

from apps.core.helpers import model_json_encoder
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import (
    TemplateResponseMixin
)
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
try:
    import simplejson as json
except ImportError:
    import json


class IndexView(generic.TemplateView):
    """Index view"""
    template_name = 'index.html'


class JSONViewMixin(TemplateResponseMixin):
    """JSON View Mixin"""
    def convert_context_to_json(self, context):
        """convert context instance to json string

        :param context: context instance (``dict``)
        :returns: ``unicode`` string , json formatted
        """
        return json.dumps(context, default=model_json_encoder)

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super(TemplateResponseMixin, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        """
        Calls delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        if self.request.is_ajax():
            return self.render_to_response({'success': True})
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        """form_valid method"""
        if self.request.is_ajax():
            return self.render_to_response(form)
        return super(JSONViewMixin, self).form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        """render_to_response

        :param context: context instance
        :param response_kwargs: response kwargs instance
        :returns: ``response`` object with ``content_type='application/json'``
        """
        if self.request.is_ajax():
            context = self.convert_context_to_json(context)
            response_kwargs.update({"content_type": 'application/json'})
            response = HttpResponse(context, **response_kwargs)
            return response
        return super(JSONViewMixin, self).render_to_response(
            context, **response_kwargs
        )


class LoginRequiredMixin(object):
    """LoginRequired View Mixin"""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)