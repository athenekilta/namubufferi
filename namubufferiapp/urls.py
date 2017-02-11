from django.conf.urls import url
from django.contrib.auth import views as auth_views

from namubufferiapp import views
from namubufferiapp.forms import MagicAuthForm, TagAuthForm
from namubufferi.settings import RECAPTCHA_SITE


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^anonymous/$', views.home_anonymous, name="home_anonymous"),
    url(r'^login', auth_views.login, {'template_name': 'namubufferiapp/base_magiclogin.html',
                                                       'extra_context': {'magic_auth_form': MagicAuthForm(),
                                                                         'tag_auth_form': TagAuthForm(),
                                                                         'recaptcha_site':RECAPTCHA_SITE,
                                                                         }}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
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
    url(r'^product/barcodes/$', views.product_barcodes,),


]
