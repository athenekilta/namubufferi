from django.urls import path
from . import views

app_name='users'
urlpatterns = [
    path('claim-balance/', views.MigrateAccountView.as_view(), name='claim_balance'),
    path('edit/<uuid:user_uuid>', views.EditUser.as_view(), name='edit_user'),
    path('sign-up/', views.SignUp.as_view(), name='signup'),
]
