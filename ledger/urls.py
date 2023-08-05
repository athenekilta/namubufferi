from django.urls import path

from . import views

app_name = "ledger"
urlpatterns = [
    path("", views.BuyView.as_view(), name="buy"),
    path("all", views.AllTransactionsView.as_view(), name="transactions"),
    path("transfer", views.TransferView.as_view(), name="transfer"),
    path("funds", views.FundsView.as_view(), name="funds"),
]
