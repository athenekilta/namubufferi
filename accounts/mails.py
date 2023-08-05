from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.conf import settings

def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = f'{settings.EMAIL_SUBJECT_PREFIX} Activate your Namubufferi account'
    message = render_to_string('registration/activate_account_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': PasswordResetTokenGenerator().make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

def send_password_reset_email(user, request):
    current_site = get_current_site(request)
    mail_subject = f'{settings.EMAIL_SUBJECT_PREFIX} Password reset on Namubufferi'
    message = render_to_string('registration/password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': PasswordResetTokenGenerator().make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()