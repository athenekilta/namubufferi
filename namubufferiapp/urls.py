from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views
from namubufferiapp.views import *


urlpatterns = [
    url(r'^$', cover, name="cover"),
    url(r'^login', auth_views.login, {'template_name': 'namubufferiapp/base_login.html',
                                                       'extra_context': dict(signin_form=AuthenticationForm(),
                                                                             register_form=UserCreationForm(),
                                                                             )}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/', }),
    url(r'^register/$', register),
    url(r'^buy/', buy_view, name="buy_view"),
    url(r'^deposit/', deposit_view, name="deposit_view"),
]
