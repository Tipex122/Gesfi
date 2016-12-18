from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import search as search_views
from .views import search_keywords

urlpatterns = [
#    url(r'^login/$', views.site_login),

    url(r'^login/$', auth_views.login, name='gesfi_login'),

#    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^search/$', search_views, name='search'),
    url(r'^keywords/$', search_keywords, name='search_keywords'),

]