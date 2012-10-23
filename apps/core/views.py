# Create your views here.
# coding: utf-8
from apps.core.helpers import render_to
from django.http import HttpResponse


@render_to('index.html')
def index(request):
    return {}


def write_redirect(request, pk):
    response = HttpResponse()
    response.write('redirected with: %s' % pk)
    return response


@render_to('index.html')
def test_redirect(request, pk):
    return {
        'redirect': 'core:write-redirect',
        'redirect-args': (pk, )
    }
