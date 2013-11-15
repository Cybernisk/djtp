from django.conf.urls import patterns, url
from apps.accounts import views
from apps.core.shortcuts import direct_to_template

urlpatterns = patterns(
    'apps.accounts.views',
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^password/(?P<sid>[\w\d]+)/restore/$',
        views.PasswordRestoreView.as_view(),
        name='password-restore'),
    url(r'^password/restore/initiate/$',
        views.PasswordRestoreInitiateView.as_view(),
        name='password-restore-initiate'),
    url(r'^profile/password/change/$',
        views.PasswordChangeView.as_view(),
        name='password-change'),
    # static
    url(r'^password/changed/$', direct_to_template,
        {'template': 'accounts/password_changed.html'},
        name='password-changed'),
    url(r'^password/restored/$', direct_to_template,
        {'template': 'static/password_restored.html'},
        name='password-restored'),
    url(r'^password/restore/initiated/$', direct_to_template,
        {'template': 'static/password_restore_initiated.html'},
        name='password-restore-initiated'),
)
