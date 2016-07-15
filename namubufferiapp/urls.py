from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from namubufferiapp.views import home_view, register_view, buy_view, deposit_view


urlpatterns = [
    url(r'^$', home_view, name="home"),
    url(r'^login', auth_views.login, {'template_name': 'namubufferiapp/base_login.html',
                                                       'extra_context': dict(register_form=UserCreationForm(),
                                                                             )}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/', }),
    url(r'^register/$', register_view),
    url(r'^buy/', buy_view, name="buy_view"),
    url(r'^deposit/', deposit_view, name="deposit_view"),
]
