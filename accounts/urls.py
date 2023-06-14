from django.urls import path, reverse_lazy

from django.contrib.auth import views as auth_views

# from .views import RegisterView, ProfileView, ProfileEditView, ProfileDeleteView

from . import views

app_name = "accounts"
urlpatterns = [
    # path("terms/", views.terms, name="terms"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    

    path("signup/", views.register_account, name="signup"),
    path("signup/activate/<uidb64>/<token>/", views.activate_account, name="activate"),

    path("password_reset/", 
        auth_views.PasswordResetView.as_view(success_url=reverse_lazy("accounts:password_reset_done")), 
            name="password_reset"),
    
    path("password_reset_sent/",
         auth_views.PasswordResetDoneView.as_view(),
            name="password_reset_done"),    
    
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("accounts:password_reset_complete")),
            name="password_reset_confirm"),
    
    path("password_reset_complete/",
         auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete"),

    # path("profile/", ProfileView.as_view(), name="profile"),
    # path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    # path("profile/delete/", ProfileDeleteView.as_view(), name="profile_delete"),
    
    path('usernames-list/', views.UsernamesAPIView.as_view(), name='usernames-list'), # Special View for the API
]