from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^$', 'categories.views.category_list', name='category_list'),
    url(r'^budget/$', views.category_list),
    url(r'^test/$', views.category_json, name='categories_json'),
]
