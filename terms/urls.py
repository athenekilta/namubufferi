from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "terms"
urlpatterns = [
    path("", views.TermsUpdateView.as_view(), name="update"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("userguide/", views.DocumentDetailView.as_view(), name="userguide"),
]
