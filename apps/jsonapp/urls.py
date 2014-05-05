from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:


urlpatterns = patterns(
    '',
    url(r'^accounts/', include('apps.accounts.urls.json',
                               namespace='accounts')),
    url(r'^core/', include('apps.core.json_urls', namespace='core'))
)
