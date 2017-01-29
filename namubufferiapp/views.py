from base64 import b64encode
from decimal import Decimal
from hashlib import sha256
from os import urandom
import re

import requests
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from .forms import MoneyForm, MagicAuthForm, TagAuthForm, ProductForm
from .models import Account, Product, Category, Transaction, UserTag, ProductTag
from namubufferi.settings import DEBUG, AUTHENTICATION_BACKENDS

@staff_member_required
def adminedit(request):
    context = dict(product_form=ProductForm(),
                   products=Product.objects.all(),
                   categories=Category.objects.all(),
                   transactions=request.user.account.transaction_set.all()
                   )

    return render(request, 'namubufferiapp/admin_handleproducts.html', context)

@staff_member_required
def product_modify(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product, created = Product.objects.get_or_create(
                                name=product_form.cleaned_data['name'],
                                defaults={'category':product_form.cleaned_data['category'],},
                            )
            product.category = product_form.cleaned_data['category']
            product.price = product_form.cleaned_data['price']
            product.inventory = product_form.cleaned_data['inventory']
            product.hidden = product_form.cleaned_data['hidden']
            product.save()

            if created:
                return HttpResponse("Product created", status=201)
            else:
                return HttpResponse("Product updated", status=200)

        else:
            return HttpResponse('{"errors":' + product_form.errors.as_json() + '}', content_type="application/json")
    else:
        raise Http404()

@staff_member_required
def product_add_barcode(request, prod_id, barcode):
    if request.method == 'PUT':
        try:
            product = Product.objects.get(pk=prod_id)
            ptag, created = ProductTag.objects.get_or_create(uid=barcode,
                                                             defaults={'product':product,},)
            ptag.product = product
            ptag.save()

            if created:
                return HttpResponse("Barcode created", status=201)
            else:
                return HttpResponse("Barcode reassigned", status=200)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=400)
    else:
        raise Http404()


def product_barcodes(request):
    barcodes = dict()
    for bcode in ProductTag.objects.all():
        barcodes[bcode.uid] = bcode.product.pk

    return JsonResponse(barcodes)

@login_required(redirect_field_name=None)
def home(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')
    else:

        context = dict(money_form=MoneyForm(),
                       products=Product.objects.all(),
                       categories=Category.objects.all(),
                       transactions=request.user.account.transaction_set.all()
                       )

    return render(request, 'namubufferiapp/base_home.html', context)

def home_anonymous(request):
    context = dict(products=Product.objects.all(),
                   categories=Category.objects.all(),
                   )

    return render(request, 'namubufferiapp/base_homeanonymous.html', context)


def buy(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=request.POST['product_key'])
        price = product.price

        new_transaction = Transaction()
        new_transaction.amount = -price
        new_transaction.product = product

        new_balance = Decimal(0)

        if request.user.is_authenticated:
            request.user.account.make_payment(price)
            new_balance = request.user.account.balance
            new_transaction.customer = request.user.account

        new_transaction.save()
        product.make_sale()

        return JsonResponse({'balance': new_balance,
                             'transactionkey': new_transaction.pk,
                             'modalMessage': "Purchase Successful",
                             'message': render_to_string('namubufferiapp/message.html',
                                                         {'message': "Purchase Successful"}),
                             })
    else:
        raise Http404()


@login_required
def deposit(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        money_form = MoneyForm(request.POST)

        if money_form.is_valid():
            euros = request.POST['euros']
            cents = request.POST['cents']
            amount = Decimal(euros) + Decimal(cents)/100

            request.user.account.make_deposit(amount)

            new_transaction = Transaction()
            new_transaction.customer = request.user.account
            new_transaction.amount = amount
            new_transaction.save()

            return JsonResponse({'balance': request.user.account.balance,
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
def transaction_history(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    return JsonResponse({'transactionhistory': render_to_string('namubufferiapp/transactionhistory.html',
                                                                {'transactions': request.user.account.transaction_set.all()[:5]})
                         })


@login_required
def receipt(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        transaction = get_object_or_404(request.user.account.transaction_set.all(),
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
def cancel_transaction(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        transaction = get_object_or_404(request.user.account.transaction_set.all(),
                                        pk=request.POST['transaction_key'])

        if (request.user == transaction.customer.user and not transaction.canceled):
            transaction.cancel()

            return JsonResponse({'balance': request.user.account.balance,
                                 'modalMessage': "Transaction Canceled",
                                 'message': render_to_string('namubufferiapp/message.html',
                                                             {'message': "Transaction Canceled",
                                                              'transaction': transaction})
                                 })
        else:
            return HttpResponse(status=204)
    else:
        raise Http404()


def magic_auth(request, magic_token=None):
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
                user = User.objects.get(email=magic_auth_form.cleaned_data['email'])
            except User.DoesNotExist:
                email = magic_auth_form.cleaned_data['email']
                m = re.match("^(.*)@aalto.fi$", email)
                if m:
                    username = m.group(1)
                    user = User.objects.create_user(username,
                                                    email=email,
                                                    password=b64encode(sha256(urandom(56)).digest()))
                else:
                    return JsonResponse({'modalMessage': 'Email not found or its not aalto email.'})


            user.account.update_magic_token()
            current_site = get_current_site(request)
            magic_link = current_site.domain + reverse('magic', kwargs={'magic_token': user.account.magic_token})

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
                print("Mail sent")
            except:
                print("Mail not sent")

            if DEBUG:
                return JsonResponse({'modalMessage': '<br><a href="http://' + magic_link + '">Login Link</a> (Sent to you email when !DEBUG)'})
            else:
                return JsonResponse({'modalMessage': 'Check your email.'})
        else:
            return HttpResponse('{"errors":' + magic_auth_form.errors.as_json() + '}', content_type="application/json")

    else:
        user = authenticate(magic_token=magic_token)
        if user:
            login(request, user)
            return render(request, 'namubufferiapp/base_authsuccess.html')
        else:
            return HttpResponse(status=410)

def tag_auth(request):
    """
    """
    if request.method == 'POST':
        # Validate form
        tag_auth_form = TagAuthForm(request.POST)
        if tag_auth_form.is_valid():
            try:
                tag_uid = tag_auth_form.cleaned_data['tag_uid']
                tag = UserTag.objects.get(uid=tag_uid)
                user = tag.user
                login(request, user, backend=AUTHENTICATION_BACKENDS[0])

                return JsonResponse({'redirect': '/'})
            except UserTag.DoesNotExist:
                return JsonResponse({'errors':{'tag_uid':
                                        [{'message':'Tag {} not found'.format(tag_uid),
                                          'code':'tagnotfound'}],}
                                    })
        else:
            return HttpResponse('{"errors":' + tag_auth_form.errors.as_json() + '}', content_type="application/json")
    else:
        return HttpResponse(status=410)

@login_required
def tag_list(request):
    tags = UserTag.objects.filter(user=request.user)

    return JsonResponse({'taglist': render_to_string('namubufferiapp/taglist.html',
                                                     {'tags': tags})
                        })

@login_required
def tag_modify(request, uid):
    if request.method == 'DELETE':
        try:
            tag = UserTag.objects.get(uid=uid)
            if tag.user == request.user:
                tag.delete()
                return HttpResponse("Tag deleted", status=200)
            else:
                raise Http404("Wrong user")
        except UserTag.DoesNotExist:
            raise Http404("Tag does not exist")

    elif request.method == 'POST':
        try:
            tag = UserTag.objects.create(user=request.user, uid=uid)
            tag.save()
            return HttpResponse("Tag created", status=201)
        except IntegrityError:
            return HttpResponse("Another tag exists ({})!".format(uid),
                                status=409)

