from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import search as search_views
from .views import search_keywords, tag_edit, tag_category_edit, transactions_by_category, transactions_of_one_category

urlpatterns = [
    url(r'^login/$', auth_views.login, name='gesfi_login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^search/$', search_views, name='search'),
    url(r'^keywords/search_keyword/$', search_keywords, name='search_keywords'),
    url(r'^tag_edit/(?P<pk>)$', tag_edit, name='tag_edit'),
    url(r'^tag_edit/(?P<pk>[0-9]+)/$', tag_edit, name = 'tag_edit'),
    url(r'^transaction_by_category/search_categories/$', tag_category_edit, name='tag_category'),
    url(r'^transactions_by_category/$', transactions_by_category, name = 'transactions_by_category'),
    url(r'^transactions_of_one_category/(?P<pk>)$', transactions_of_one_category, name='transactions_of_one_category'),
    url(r'^transactions_of_one_category/(?P<pk>[0-9]+)/$', transactions_of_one_category, name='transactions_of_one_category'),
    #TODO: See possibility to use only one function for 'transactions_by_category' & 'transactions_of_one_category'
#    url(r'^transactions_by_category/(?P<pk>[0-9]+)/$', transactions_of_one_category, name='transactions_of_one_category'),
#    url(r'^transactions_by_category/(?P<pk>)$', transactions_of_one_category, name='transactions_of_one_category'),

]