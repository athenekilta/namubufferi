from django.urls import path

from . import views

app_name = "keycards"
urlpatterns = [
    path(f"", views.KeycardLoginFormView.as_view(), name="login"),
]
