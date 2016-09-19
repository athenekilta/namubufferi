import requests

from django.shortcuts import render, get_object_or_404, redirect
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site

from django.http import JsonResponse, HttpResponse, Http404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives

from models import UserProfile, Product, Category, Transaction
from forms import MoneyForm, MagicAuthForm

from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from base64 import b64encode
from hashlib import sha256
from os import urandom

from namubufferi.settings import DEBUG


@login_required
def home_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')
    else:
        context = dict(money_form=MoneyForm(),
                       products=Product.objects.all(),
                       categories=Category.objects.all(),
                       transactions=request.user.userprofile.transaction_set.all()
                       )

    return render(request, 'namubufferiapp/base_home.html', context)


@login_required
def buy_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=request.POST['product_key'])
        price = product.price
        request.user.userprofile.make_payment(price)

        new_transaction = Transaction()
        new_transaction.customer = request.user.userprofile
        new_transaction.amount = -price
        new_transaction.product = product
        new_transaction.save()

        product.make_sale()

        return JsonResponse({'balance': request.user.userprofile.balance,
                             'transactionkey': new_transaction.pk,
                             'modalMessage': "Purchase Successful",
                             'message': render_to_string('namubufferiapp/message.html',
                                                         {'message': "Purchase Successful"}),
                             })
    else:
        raise Http404()


@login_required
def deposit_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        money_form = MoneyForm(request.POST)

        if money_form.is_valid():
            euros = request.POST['euros']
            cents = request.POST['cents']
            amount = Decimal(euros) + Decimal(cents)/100

            request.user.userprofile.make_deposit(amount)

            new_transaction = Transaction()
            new_transaction.customer = request.user.userprofile
            new_transaction.amount = amount
            new_transaction.save()

            return JsonResponse({'balance': request.user.userprofile.balance,
                                 'transactionkey': new_transaction.pk,
                                 'modalMessage': "Deposit Successful",
                                 'message': render_to_string('namubufferiapp/message.html',
                                                             {'message': "Deposit Successful",
                                                              'transaction': new_transaction,
                                                              }),
                                 })
        else:
            # https://docs.djangoproject.com/en/1.10/ref/forms/api/#django.forms.Form.errors.as_json
            # https://docs.djangoproject.com/ja/1.9/ref/request-response/#jsonresponse-objects
            #return JsonResponse({"errors": + money_form.errors.as_json()})
            # FTS...
            return HttpResponse('{"errors":' + money_form.errors.as_json() + '}', content_type="application/json")
    else:
        raise Http404()


@login_required
def transaction_history_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    return JsonResponse({'transactionhistory': render_to_string('namubufferiapp/transactionhistory.html',
                                                                {'transactions': request.user.userprofile.transaction_set.all()[:5]})
                         })


@login_required
def receipt_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        transaction = get_object_or_404(request.user.userprofile.transaction_set.all(),
                                        pk=request.POST['transaction_key'])

        receipt = {'customer': transaction.customer.user.username,
                   'amount': transaction.amount,
                   'timestamp': transaction.timestamp,
                   'transactionkey': transaction.pk,
                   'canceled': transaction.canceled,
                   }
        try:
            receipt['product'] = transaction.product.name
        except:
            receipt['product'] = 'Deposit'

        return JsonResponse({'receipt': receipt})

    else:
        raise Http404()


@login_required
def cancel_transaction_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        transaction = get_object_or_404(request.user.userprofile.transaction_set.all(),
                                        pk=request.POST['transaction_key'])

        if (request.user == transaction.customer.user and not transaction.canceled):
            transaction.cancel()

            return JsonResponse({'balance': request.user.userprofile.balance,
                                 'modalMessage': "Transaction Canceled",
                                 'message': render_to_string('namubufferiapp/message.html',
                                                             {'message': "Transaction Canceled",
                                                              'transaction': transaction})
                                 })
        else:
            return HttpResponse(status=204)
    else:
        raise Http404()


def register_view(request):
    """
    Check for further dev:
    http://www.djangobook.com/en/2.0/chapter14.html
    http://ipasic.com/article/user-registration-and-email-confirmation-django/
    https://docs.djangoproject.com/en/1.7/topics/email/

    """

    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            print request.POST
            new_user = register_form.save()

            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.save()

            return JsonResponse({'modalMessage': "Register Success. You can now sign in.",
                                 'message': render_to_string('namubufferiapp/message.html',
                                                             {'message': "Register Success. You can now sign in."})
                                 })
        else:
            return HttpResponse('{"errors":' + register_form.errors.as_json() + '}', content_type="application/json")

    else:
        raise Http404()


def magic_auth_view(request, **kwargs):
    """
    """
    if request.method == 'POST':
        # Validate reCAPTCHA
        # https://developers.google.com/recaptcha/docs/verify
        # http://docs.python-requests.org/en/master/user/quickstart/#more-complicated-post-requests
        # http://docs.python-requests.org/en/master/user/quickstart/#json-response-content
        payload = {"secret": "6LfUqSgTAAAAACc5WOqVLLmJP_3SC3bWp094D0vo",
                   "response": request.POST['g-recaptcha-response']}
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload).json()
        # TODO: Check if we need headers
        if not r['success']:
            print ("reCAPTCHA validation failed.")
            if not DEBUG:
                return JsonResponse({'modalMessage': 'Check yourself you might be a robot. Try again.'})

        # Validate form
        magic_auth_form = MagicAuthForm(request.POST)
        if magic_auth_form.is_valid():
            # Try to find the user or create a new one
            try:
                user = User.objects.get(username=request.POST['aalto_username'])
            except:  # DoesNotExist
                new_user = User.objects.create_user(request.POST['aalto_username'],
                                                    request.POST['aalto_username'] + '@aalto.fi',
                                                    b64encode(sha256(urandom(56)).digest()))

                new_profile = UserProfile()
                new_profile.user = new_user
                new_profile.magic_token_ttl = timezone.now() + timedelta(minutes=15)
                new_profile.save()
                user = new_user

            user.userprofile.update_magic_token()
            current_site = get_current_site(request)
            magic_link = current_site.domain + reverse('magic', kwargs={'magic': user.userprofile.magic_token})

            # Send mail to user
            mail = EmailMultiAlternatives(
              subject="Namubufferi - Login",
              body=("Hello. Authenticate to Namubufferi using this link. It's valid for 15 minutes.\n"
                    + magic_link),
              from_email="<namubufferi@athene.fi>",
              to=[user.email]
            )
            mail.attach_alternative(("<h1>Hello."
                                    "</h1><p>Authenticate to Namubufferi using this link. It's valid for 15 minutes.</p>"
                                    '<a href="http://' + magic_link + '"> Magic Link </a>'
                                    ), "text/html")
            try:
                mail.send()
                print "Mail sent"
            except:
                print "Mail not sent"

            if DEBUG:
                return JsonResponse({'modalMessage': 'Check your email.<br><a href="http://' + magic_link + '"> Magic Link </a>'})
            else:
                return JsonResponse({'modalMessage': 'Check your email.'})
        else:
            return HttpResponse('{"errors":' + magic_auth_form.errors.as_json() + '}', content_type="application/json")

    else:
        user = authenticate(magic_token=kwargs.get('magic'))
        if user:
            login(request, user)
            return render(request, 'namubufferiapp/base_authsuccess.html')
        else:
            return HttpResponse(status=410)
