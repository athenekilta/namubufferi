from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'namubufferi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('namubufferiapp.urls')),
]
