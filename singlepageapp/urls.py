from django.urls import path

from . import views

app_name = "singlepageapp"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("config", views.Config.as_view(), name="config"),
]
