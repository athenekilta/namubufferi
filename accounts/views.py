from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import (
    UserRegisterForm, ProfileForm,
    ProfileChangePasswordForm, 
    ProfileDeleteForm, PasswordResetForm
)
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser as User, TermsOfService, PrivacyPolicy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import PasswordResetTokenGenerator 

class RegisterView(FormView):
    """
    View for registering a new user account.
    """
    template_name = 'registration/signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('ledger:buy')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:login')

class ProfileView(FormView):
    """
    View for viewing user profile.
    """
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('ledger:buy')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ProfileChangePasswordView(FormView):
    """
    View for editing user password profile.
    """
    template_name = 'registration/profile_change_password.html'
    form_class = ProfileChangePasswordForm
    success_url = reverse_lazy('ledger:buy')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        user = authenticate(username=self.request.user.username, password=form.cleaned_data['new_password1'])
        login(self.request, user)
        return super().form_valid(form)
    
class ProfileDeleteView(FormView):
    """
    View for deleting user profile.
    """
    template_name = 'registration/profile_delete.html'
    form_class = ProfileDeleteForm
    success_url = reverse_lazy('accounts:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save(self.request.user)
        messages.success(self.request, 'Your account has been deleted!')
        return super().form_valid(form)

class PasswordResetView(FormView):
    """
    View for resetting user password.
    """
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    form_class = PasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class TermsView(TemplateView):
    """
    View for viewing terms of service.
    """
    template_name = 'registration/terms.html'
    model = TermsOfService
    context_object_name = 'terms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = TermsOfService.objects.first()
        return context

class PrivacyView(TemplateView):
    """
    View for viewing privacy policy.
    """
    template_name = 'registration/privacy.html'
    model = PrivacyPolicy
    context_object_name = 'privacy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacy'] = PrivacyPolicy.objects.first()
        return context
    