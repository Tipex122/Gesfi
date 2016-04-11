from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
#    url(r'^login/$', views.site_login),

    url(r'^login/$', auth_views.login, name='gesfi_login'),

#    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),


]