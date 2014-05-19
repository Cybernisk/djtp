from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.core.json_views',
    url(r'^timezone/(?P<domain>[\w\-_]+)/(?P<zone>[\w\-_]+)/$', 'timezone_now',
        name='timezone-now'),
)

