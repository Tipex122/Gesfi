"""gesfi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin, auth
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^', include('categories.urls')),
    url(r'^', include('banksandaccounts.urls')),
    url(r'^', include('managegesfi.urls')),

    #Deprecated
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='gesfi_login'),

#Good sans pointer sur managegesfi.urls
    #    url(r'^login/$', auth_views.login, name='gesfi_login'),

    #Deprecated
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

#Good sans pointer sur managegesfi.urls
    # url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
]
