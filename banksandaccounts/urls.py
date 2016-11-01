from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^$', 'categories.views.category_list', name='category_list'),
    url(r'^$', views.transactions_list, name='transactions_list'),
    url(r'^transaction_detail/(?P<transaction_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^account/(?P<account_id>[0-9]+)/$', views.account_list, name='account_list'),
]