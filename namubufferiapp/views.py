from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from .models import UserProfile
import datetime
import random
import hashlib


def cover(request):
    context = dict(backend_form=AuthenticationForm(),
                   signin_form=AuthenticationForm(),
                   register_form=UserCreationForm(),
                   user_photos=[],
                   browse_photos=[],
                   scroll_to="",
                   upload_message="",
                   register_message="",
                   permalink_key=""
                   )

    return render(request, 'namubufferiapp/base.html', context)
    if request.method == 'POST':
        backend_form = AuthenticationForm(request.POST, request.FILES)
        context['backend_form'] = backend_form
        context['posted'] = backend_form.instance
        if backend_form.is_valid():
            new_photo = backend_form.save(commit=False)
            # Create img key:
            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + backend_form.cleaned_data.get('title')).encode('utf8')
            img_key = hashlib.sha1(salted).hexdigest()
            new_photo.img_key = img_key
            print(img_key)

            if request.user.is_authenticated():
                new_photo.user = request.user
                new_photo.save()
            else:
                new_photo.save()
                context['anon_upload_photo'] = [new_photo]
            context['scroll_to'] = "#user"
            context['upload_message'] = "Upload complete."

    return render(request, 'namubufferiapp/base.html', context)


def register(request):
    """
    Check:
    http://www.djangobook.com/en/2.0/chapter14.html
    http://ipasic.com/article/user-registration-and-email-confirmation-django/
    https://docs.djangoproject.com/en/1.7/topics/email/

    """
    context = dict(backend_form=AuthenticationForm(),
                   signin_form=AuthenticationForm(),
                   register_form=UserCreationForm(),
                   user_photos=[],
                   browse_photos=[],
                   scroll_to="",
                   upload_message="",
                   register_message="",
                   permalink_key=""
                   )

    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        context['register_form'] = register_form
        if register_form.is_valid():
            new_user = register_form.save()
            # Create a placeholder for a profile. Currently not in use.
            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.save()
            context['scroll_to'] = ""
            context['register_message'] = "You can now sign in with the account."

    return render(request, 'namubufferiapp/base.html', context)


def buy_view(request, product_key):
    # TODO

    context = dict(backend_form=AuthenticationForm(),
                   signin_form=AuthenticationForm(),
                   register_form=UserCreationForm(),
                   user_photos=[],
                   browse_photos=[],
                   scroll_to="",
                   upload_message="",
                   register_message="",
                   permalink_key=""
                   )
    return render(request, 'namubufferiapp/base.html', context)
