from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'categories.views.category_list', name='category_list'),
]