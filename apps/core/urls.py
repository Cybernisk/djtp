from django.conf.urls import patterns, include, url
from apps.core.shortcuts import direct_to_template


urlpatterns = patterns(
    'apps.core.views',
    url('^$', 'index', name='index'),
    url('^test/(?P<pk>\d+)/redirect/$', 'test_redirect',
        name='test-redirect'),
    url('^show/(?P<pk>\d+)/redirect/$', 'write_redirect',
        name='write-redirect'),
    # static urls with info
    url('^permission/denied/$', direct_to_template,
        {'template': 'core/blockage.html'},
        name='blockage'),
)

