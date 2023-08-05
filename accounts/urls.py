from django.urls import path, reverse_lazy

from django.contrib.auth import views as auth_views

# from .views import RegisterView, ProfileView, ProfileEditView, ProfileDeleteView

from . import views

app_name = "accounts"
urlpatterns = [
      path("login/", auth_views.LoginView.as_view(), name="login"),
      path("logout/", auth_views.LogoutView.as_view(), name="logout"),
      

      path("signup/", views.RegisterView.as_view(), name="signup"),
      path("signup/activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),

      path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
      
      path("password_reset_sent/",
            auth_views.PasswordResetDoneView.as_view(),
               name="password_reset_done"),    
      
      path("reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("accounts:password_reset_complete")),
               name="password_reset_confirm"),
      
      path("password_reset_complete/",
            auth_views.PasswordResetCompleteView.as_view(),
               name="password_reset_complete"),

      path("profile/", views.ProfileView.as_view(), name="profile"),
      path("profile/change_password/", views.ProfileChangePasswordView.as_view(), name="profile_change_password"),
      path("profile/delete/", views.ProfileDeleteView.as_view(), name="profile_delete_account"),
      
      path("terms/", views.TermsView.as_view(), name="terms"),
      path("privacy/", views.PrivacyView.as_view(), name="privacy"),
]