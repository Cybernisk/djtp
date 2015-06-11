from django.conf.urls import patterns, url
from apps.core import views
from apps.core.shortcuts import direct_to_template


urlpatterns = patterns(
    'apps.core.views',
    url('^$', views.IndexView.as_view(), name='index'),
    # static urls with info
    url('^permission/denied/$', direct_to_template,
        {'template': 'core/blockage.html'},
        name='blockage'),
)
