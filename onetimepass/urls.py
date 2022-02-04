from django.urls import path

from . import views

app_name = "onetimepass"
urlpatterns = [
    path(
        "",
        views.OneTimePassCreateView.as_view(),
        name="login",
    ),
    path("email-test/", views.EmailTemplateView.as_view()),
    path(
        "<uuid:pk>/",
        views.OneTimePassCheckFormView.as_view(),
        name="check",
    ),
]
