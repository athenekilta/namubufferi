from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm

from namubufferiapp import views
from namubufferiapp.forms import MagicAuthForm, TagAuthForm


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login', auth_views.login, {'template_name': 'namubufferiapp/base_magiclogin.html',
                                                       'extra_context': {'register_form': UserCreationForm(),
                                                                         'magic_auth_form': MagicAuthForm(),
                                                                         'tag_auth_form': TagAuthForm(),
                                                                         }}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^register/$', views.register, name="register"),
    url(r'^buy/$', views.buy, name="buy"),
    url(r'^deposit/$', views.deposit, name="deposit"),
    url(r'^cancel/$', views.cancel_transaction, name="cancel"),
    url(r'^receipt/$', views.receipt, name="receipt"),
    url(r'^history/$', views.transaction_history, name="history"),
    url(r'^magic/$', views.magic_auth),
    url(r'^magic/(?P<magic_token>.*)/$', views.magic_auth, name="magic"),
    url(r'^tag/auth/$', views.tag_auth, name="tag_auth"),
    url(r'^tag/$', views.tag_list),
    url(r'^tag/(?P<uid>.*)/$', views.tag_modify),

    url(r'^productmodify/$', views.adminedit),
    url(r'^product/update/$', views.product_modify, name="product_update"),
    url(r'^product/(?P<prod_id>.*)/barcode/(?P<barcode>.*)$', views.product_add_barcode,),


]
