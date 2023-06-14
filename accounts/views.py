from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import CustomUser as User, PassPhrase
from django.core.mail import EmailMessage
from rest_framework.generics import ListAPIView
from .serializers import UsernameSerializer

class UsernamesAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsernameSerializer

def register_account(request):
    """
    View for registering a new user account.
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            messages.success(request, 'Your account has been created! Check your email to finish the registration.')
            return redirect('accounts:login')
    else:
        user_form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': user_form, 'title': 'Register'})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('ledger:index')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:login')

def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Active your Namubufferi account.'
    message = render_to_string('registration/activate_account_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()