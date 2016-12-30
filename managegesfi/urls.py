from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import search as search_views
from .views import search_keywords, tag_edit

urlpatterns = [
#    url(r'^login/$', views.site_login),

    url(r'^login/$', auth_views.login, name='gesfi_login'),

#    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^search/$', search_views, name='search'),
    url(r'^keywords/search_keyword/$', search_keywords, name='search_keywords'),
    url(r'^tag_edit/(?P<pk>)$', tag_edit, name='tag_edit'),
    url(r'^tag_edit/(?P<pk>[0-9]+)/$', tag_edit, name = 'tag_edit'),

    #    url(r'^tag_edit/(?P<pk>(\d+))/$', tag_edit, name='tag_edit'),

]