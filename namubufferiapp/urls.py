from django.conf.urls import include, url

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm

from namubufferiapp.forms import MagicAuthForm

from namubufferiapp.views import home_view, register_view, buy_view, deposit_view
from namubufferiapp.views import cancel_transaction_view, receipt_view, transaction_history_view
from namubufferiapp.views import magic_auth_view


urlpatterns = [
    url(r'^$', home_view, name="home"),
    url(r'^login', auth_views.login, {'template_name': 'namubufferiapp/base_magiclogin.html',
                                                       'extra_context': {'register_form': UserCreationForm(),
                                                                         'magic_auth_form': MagicAuthForm(),
                                                                         }}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^register/$', register_view, name="register"),
    url(r'^buy/$', buy_view, name="buy"),
    url(r'^deposit/$', deposit_view, name="deposit"),
    url(r'^cancel/$', cancel_transaction_view, name="cancel"),
    url(r'^receipt/$', receipt_view, name="receipt"),
    url(r'^history/$', transaction_history_view, name="history"),
    url(r'^magic/$', magic_auth_view),
    url(r'^magic/(?P<magic_token>.*)/$', magic_auth_view, name="magic"),
]
