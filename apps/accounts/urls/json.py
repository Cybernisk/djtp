from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'apps.accounts.views.json',
    url(r'users/$', 'users', name='users'),
)
