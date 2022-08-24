from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import FormView, CreateView, UpdateView

from django import utils
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from .forms import ClaimBalanceForm, CreateUserForm, ManageUserForm


User = get_user_model()

class MigrateAccountView(FormView):
    """View for users to claim their existing balance"""
    form_class = ClaimBalanceForm
    template_name = 'users/claimbalance.html'
    

    def form_valid(self, form):
        data = form.cleaned_data['name_in_namubuffa'].split(' ')

        if len(data) > 1:
            first_name = data[0]
            last_name = data[1]
        
        email = form.cleaned_data['email']

        username = first_name.lower() if not last_name else f"{first_name.lower()}.{last_name.lower()}"

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user and user.last_login is None:
            user.email = email
            user.save()

            base64_encoded_id = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url_args = {'uidb64': base64_encoded_id, 'token': token}
            reset_path = reverse('password_reset_confirm', kwargs=reset_url_args)
            reset_url = f'{settings.BASE_URL}{reset_path}'

            send_mail(
                "Welcome to namubufferi!", 
                message=f"Reset your password \n Your username: {user.username} \n Password reset link: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email]
            )

        return redirect('landing:index')


class SignUp(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class EditUser(UpdateView):
    model = get_user_model()
    form_class = ManageUserForm
    slug_field = 'pk'
    slug_url_kwarg = 'user_uuid'
    success_url = reverse_lazy('singlepageapp:index')
    template_name = 'users/edit_user.html'