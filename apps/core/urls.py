from django.conf.urls import url
from apps.core import views
from django.views.generic import TemplateView


urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    # static urls with info
    url('^permission/denied/$', TemplateView.as_view(
        template_name= 'core/blockage.html'),
        name='blockage'),
]
