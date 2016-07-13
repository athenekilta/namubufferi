from django.shortcuts import render, get_object_or_404, redirect
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from models import UserProfile, Product, Category
from forms import MoneyForm


# TODO: Remve unused
global_context = dict(signin_form=AuthenticationForm(),
                      register_form=UserCreationForm(),
                      money_form=MoneyForm(),
                      products=Product.objects.all(),
                      categories=Category.objects.all(),
                      message="",
                      )


def cover(request):
    context = global_context.copy()
    return render(request, 'namubufferiapp/base.html', context)


def register(request):
    """
    Check:
    http://www.djangobook.com/en/2.0/chapter14.html
    http://ipasic.com/article/user-registration-and-email-confirmation-django/
    https://docs.djangoproject.com/en/1.7/topics/email/

    """
    context = global_context.copy()

    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        context['register_form'] = register_form
        if register_form.is_valid():
            new_user = register_form.save()
            # Create a placeholder for a profile. Currently not in use.
            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.save()
            context['message'] = 'Rekisteroityminen onnistui. Voit kirjautua sisaan.'

    return render(request, 'namubufferiapp/base.html', context)


@login_required
def buy_view(request, product_key):
    context = global_context.copy()

    product = get_object_or_404(Product, pk=product_key)
    price = product.price
    request.user.userprofile.make_payment(price)
    context['message'] = 'Ostit ' + str(price)

    return render(request, 'namubufferiapp/base.html', context)


@login_required
def deposit_view(request, amount):
    context = global_context.copy()

    if request.method == 'POST':
        money_form = MoneyForm(request.POST)
        context['money_form'] = money_form
    if money_form.is_valid():
        amount = request.POST['amount']
        request.user.userprofile.make_deposit(amount)
        context['message'] = 'Lisasit ' + str(amount)

    return render(request, 'namubufferiapp/base.html', context)
