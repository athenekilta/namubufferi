from django.conf.urls import url
from django.contrib.auth import views as auth_views

from namubufferiapp import views

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^admin/inventory/$", views.admin_inventory, name="admin_inventory"),
    url(r"^admin/overview/$", views.admin_overview, name="admin_overview"),
    url(r"^anonymous/$", views.home_anonymous, name="home_anonymous"),
    url(r"^buy/$", views.buy, name="buy"),
    url(r"^cancel/$", views.cancel_transaction, name="cancel"),
    url(r"^deposit/$", views.deposit, name="deposit"),
    url(r"^history/$", views.transaction_history, name="history"),
    url(r"^login/$", views.login_view, name="login"),
    url(r"^logout/$", auth_views.logout, name="logout"),
    url(r"^magic/$", views.magic_auth, name="magic_login"),
    url(r"^magic/(?P<magic_token>.*)/$", views.magic_auth, name="magic"),
    url(
        r"^product/(?P<prod_id>.*)/barcode/(?P<barcode>.*)/$", views.product_add_barcode
    ),
    url(
        r"^product/barcode/discover/(?P<barcode>.*)/$",
        views.discover_barcode,
        name="discover_barcode",
    ),
    url(r"^product/barcodes/$", views.list_barcodes),
    url(r"^product/update/$", views.product_update, name="product_update"),
    url(r"^receipt/$", views.receipt, name="receipt"),
    url(r"^tag/$", views.tag_list),
    url(r"^tag/(?P<uid>.*)/$", views.tag_modify),
    url(r"^tag/auth/$", views.tag_auth, name="tag_auth"),
    url(r"^tos/$", views.tos, name="tos"),
]
