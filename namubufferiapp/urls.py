from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views
from namubufferiapp.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'namubufferi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', cover, name="cover"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'namubufferiapp/base.html',
                                                         'extra_context': {'register_form': UserCreationForm}}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', }),
    url(r'^register/$', register),
    url(r'^buy/(?P<product_key>\w+)/$', buy_view, name="buy_view"),
)
