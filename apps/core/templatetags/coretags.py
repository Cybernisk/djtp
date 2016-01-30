# coding: utf-8
import importlib
from django.template import Library, Node, TemplateSyntaxError

register = Library()


class GetFormNode(Node):
    def __init__(self, init, varname, use_request):
        self.init = init[1:-1]
        self.varname = varname
        self.use_request = use_request

    def render(self, context):
        app, form_class = self.init.rsplit('.', 1)
        module = importlib.import_module(app)
        form_class = getattr(module, form_class)
        context[self.varname] = form_class(request=context['request']) \
            if self.use_request else form_class()
        return ''


@register.tag
def get_form(parser, tokens):
    """
    Get form filter servers for get form instance from inside template

    Usage::

        {% get_form 'apps.accounts.forms.LoginForm' as form %}
        {{ form.as_ul }}

    """
    bits = tokens.contents.split()
    if len(bits) != 4 and len(bits) != 5:
        raise (TemplateSyntaxError,
               "get_form  'app.model.Form' for form [use_request]")
    if bits[2] != 'as':
        raise TemplateSyntaxError("the second argument must be 'as'")
    init = bits[1]
    varname = bits[3]
    use_request = bool(bits[4]) if len(bits) > 4 else False
    return GetFormNode(init, varname, use_request)
