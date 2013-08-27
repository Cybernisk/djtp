from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    url(r'^accounts/', include('apps.accounts.urls.json', namespace='accounts')),
)
