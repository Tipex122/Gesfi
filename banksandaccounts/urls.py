from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.transactions_list2, name='transactions_list2'),
    url(r'^toto/$', views.TransactionsListView.as_view(), name='transactions_list'),
    url(r'^transaction_detail/(?P<transaction_id>[0-9]+)/$', views.transaction_detail, name='transaction_detail'),
    url(r'^account/(?P<account_id>[0-9]+)/$', views.account_list, name='account_list'),
    url(r'^banks_and_accounts_list/$', views.banks_and_accounts_list, name='banks_and_accounts_list'),
    #    url(r'^keywords/(?P<tag_name>[a-z,\',\*,A-Z]+)/$',
    #    views.transactions_with_tag, name='transactions_with_tag'),
]
