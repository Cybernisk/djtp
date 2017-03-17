from django.conf.urls import url
from apps.accounts import views
from django.views.generic import TemplateView

urlpatterns = [
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
    url(r'^password/changed/$', TemplateView.as_view(
        template_name='accounts/password_changed.html'),
        name='password-changed'),
    url(r'^password/restored/$', TemplateView.as_view(
        template_name= 'static/password_restored.html'),
        name='password-restored'),
    url(r'^password/restore/initiated/$', TemplateView.as_view(
        template_name= 'static/password_restore_initiated.html'),
        name='password-restore-initiated'),
]