from django.urls import path

from . import views

app_name = "ledger"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all", views.AllTransactionsView.as_view(), name="all"),
    path("buy", views.BuyProductView.as_view(), name="buy"),
    path("transfer", views.TransferView.as_view(), name="transfer"),
    path("funds", views.add_funds, name="funds"),
    path('product-list', views.ProductListAPIView.as_view(), name='product-list'), # Special View for the API

]
