from django.conf.urls import url
from django.contrib.auth import views as auth_views

from namubufferiapp import views

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^buy/$", views.buy, name="buy"),
    url(r"^cancel/$", views.cancel_transaction, name="cancel"),
    url(r"^deposit/$", views.deposit, name="deposit"),
    url(r"^history/$", views.transaction_history, name="history"),
    url(r"^login/$", views.magic_login, name="magic-login"),
    url(r"^logout/$", auth_views.logout, name="logout"),
    url(r"^magic/(?P<magic_token>.*)/$", views.magic_auth, name="magic-auth"),
    url(r"^receipt/$", views.receipt, name="receipt"),
]
