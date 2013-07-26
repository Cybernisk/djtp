from django.conf.urls import patterns, include, url
from apps.core.shortcuts import direct_to_template

urlpatterns = patterns('apps.accounts.views',
    url(r'login/$', 'login', name='login'),
    url(r'logout/$', 'logout', name='logout'),
    url(r'password/(?P<sid>[\w\d]+)/restore/$', 'password_restore',
        name='password-restore'),
    url(r'password/restore/initiate/$', 'password_restore_initiate',
        name='password-restore-initiate'),
    url(r'profile/password/change/$', 'password_change',
        name='password-change'),
    # static
    url(r'password/changed/$', direct_to_template,
        {'template': 'accounts/password_changed.html'},
        name='password-changed'),
    url(r'^password/restored/$', direct_to_template,
        {'template': 'static/password_restored.html'},
        name='password-restored'),
    url(r'^password/restore/initiated/$', direct_to_template,
        {'template': 'static/password_restore_initiated.html'},
        name='password-restore-initiated'),
)
