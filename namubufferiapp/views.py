from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from .models import UserProfile, Product
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
                   permalink_key="",
                   products=[]
                   )
    context['products'] = Product.objects.all()
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

    price = 1  # TODO: Get price with product_key form products
    request.user.userprofile.make_payment(price)
    return render(request, 'namubufferiapp/base.html', context)


def deposit_view(request, amount):
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

    amount = 1  # TODO
    request.user.userprofile.make_deposit(amount)
    return render(request, 'namubufferiapp/base.html', context)
