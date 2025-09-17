from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.urls import path

from jsonapi.urls import generic_path_set
from ledger.models import Account, Barcode, Group, Product, Transaction

User = get_user_model()

from . import views

app_name = "api"
urlpatterns = [
    path("", views.UserRedirectView.as_view(), name="index"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("balances/", views.BalanceListView.as_view(), name="debts"),
    path("debts/", views.DebtListView.as_view(), name="debts"),
    *generic_path_set(Account, views, pk_url_kwarg="uuid:pk"),
    *generic_path_set(Barcode, views, pk_url_kwarg="int:pk"),
    *generic_path_set(Group, views, pk_url_kwarg="uuid:pk"),
    *generic_path_set(Product, views, pk_url_kwarg="uuid:pk"),
    *generic_path_set(Transaction, views, pk_url_kwarg="uuid:pk"),
    *generic_path_set(User, views, pk_url_kwarg="uuid:pk"),
]
