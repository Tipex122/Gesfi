from django.conf.urls import url

from .views import *

urlpatterns = [
#    url(r'^$', 'categories.views.category_list', name='category_list'),
    url(r'^budget/$', category_list, name='budget'),
    url(r'^test/$', category_json, name='categories_json'),

    url(r'^tags/search_tags/$', search_tags, name='search_tags'),

    url(r'^tag_edit/(?P<pk>)$', tag_edit, name='tag_edit'),
    url(r'^tag_edit/(?P<pk>[0-9]+)/$', tag_edit, name='tag_edit'),
]
