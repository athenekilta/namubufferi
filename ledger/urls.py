from django.urls import path

from . import views

app_name = "ledger"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all", views.AllTransactionsView.as_view(), name="all"),
    path("buy", views.BuyProductView.as_view(), name="buy"),
    path("transfer", views.TransferView.as_view(), name="transfer"),
    path("add", views.AddFundsView.as_view(), name="add"),
    path('product-list/', views.ProductListAPIView.as_view(), name='product-list'), # Special View for the API
]
