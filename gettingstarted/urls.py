from django.conf.urls import url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import deauthorized.views

urlpatterns = [
    url(r'^$', deauthorized.views.index, name='index'),
    url(r'^auth', deauthorized.views.auth, name='auth'),
    url(r'^logout', deauthorized.views.logout, name='logout'),
    url(r'^openid_auth_callback', deauthorized.views.auth_callback,
        name='openid_auth_callback'),
    url(r'^end_session_callback', deauthorized.views.end_session_callback,
        name='end_session_callback'),
    path('admin/', admin.site.urls),
]

from django.contrib.auth import logout
