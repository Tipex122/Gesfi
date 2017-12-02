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
from django.conf import settings

# from django.core.urlresolvers import reverse_lazy
# from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),

    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^', include('categories.urls')),
    url(r'^', include('banksandaccounts.urls')),
    url(r'^', include('managegesfi.urls')),
    # url(r'xadmin/', include(xadmin.site.urls)),
]

# TODO: debug_toolbar doesn't work with __debug__/ adress ????
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
