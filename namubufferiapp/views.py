import json
import re
import urllib.request
from base64 import b64encode
from decimal import Decimal
from hashlib import sha256
from os import urandom

from bs4 import BeautifulSoup
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives, mail_admins
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from namubufferi import settings

from .backends import add_tag_to_user
from .forms import MagicAuthForm, MoneyForm, ProductForm, TagAuthForm
from .models import Category, Product, ProductTag, Transaction, UserTag


@staff_member_required
def admin_inventory(request):
    """
    View to handle stocking up inventory, adding products...
    """
    context = dict(
        product_form=ProductForm(),
        products=Product.objects.all(),
        categories=Category.objects.all(),
        transactions=request.user.account.transaction_set.all(),
    )

    return render(request, "namubufferiapp/admin_handleinventory.html", context)


@staff_member_required
def admin_overview(request):
    """
    Most important things at a glance for admins
    """
    positive_users = [x for x in User.objects.all() if x.account.balance >= 0]
    negative_users = [x for x in User.objects.all() if x.account.balance < 0]

    positive_balance = Decimal(0)
    for u in positive_users:
        positive_balance += u.account.balance
    negative_balance = Decimal(0)
    for u in negative_users:
        negative_balance += -u.account.balance

    context = dict(
        products=Product.objects.all(),
        positive_users=positive_users,
        positive_balance=positive_balance,
        negative_users=negative_users,
        negative_balance=negative_balance,
        overall_balance=positive_balance - negative_balance,
    )

    return render(request, "namubufferiapp/admin_overview.html", context)


@staff_member_required
def product_update(request):
    """
    Update or create product
    """
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product, created = Product.objects.get_or_create(
                name=product_form.cleaned_data["name"],
                defaults={
                    "category": product_form.cleaned_data["category"],
                },
            )
            product.category = product_form.cleaned_data["category"]
            product.price = product_form.cleaned_data["price"]
            product.inventory = product_form.cleaned_data["inventory"]
            product.hidden = product_form.cleaned_data["hidden"]
            product.save()

            bcode = product_form.cleaned_data["barcode"]
            if bcode is not None:
                ptag, ptagcreated = ProductTag.objects.get_or_create(
                    uid=bcode,
                    defaults={
                        "product": product,
                    },
                )
                ptag.product = product
                ptag.save()

            if created:
                return HttpResponse("Product created", status=201)
            else:
                return HttpResponse("Product updated", status=200)

        else:
            return HttpResponseBadRequest(
                '{"errors":' + product_form.errors.as_json() + "}",
                content_type="application/json",
            )
    else:
        raise Http404()


@staff_member_required
def product_add_barcode(request, prod_id, barcode):
    if request.method == "PUT":
        try:
            product = Product.objects.get(pk=prod_id)
            ptag, created = ProductTag.objects.get_or_create(
                uid=barcode,
                defaults={
                    "product": product,
                },
            )
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


def list_barcodes(request):
    barcodes = dict()
    for bcode in ProductTag.objects.all():
        barcodes[bcode.uid] = bcode.product.pk

    return JsonResponse(barcodes)


def product_from_outpan(barcode):
    """
    Try to guess product name from barcode using outpan.com

    False if no name was found
    """
    try:
        from namubufferi.settings import OUTPAN_API_KEY

        result = urllib.request.urlopen(
            "https://api.outpan.com/v2/products/{}?apikey={}".format(
                barcode, OUTPAN_API_KEY
            )
        )
        if result.getcode() != 200:
            return False

        name = json.loads(result.read().decode())["name"]

        if name is None:
            return False
        else:
            return name
    except:
        return False


def product_from_foodie(barcode):
    """
    Try to guess product name from barcode using foodie.fi
    False if no name was found.

    Use of this might not be ok by EULA, but shouldn't really hurt anybody
    """
    try:
        result = urllib.request.urlopen(
            "https://www.foodie.fi/entry/{}".format(barcode)
        )
        if result.getcode() != 200:
            return False

        soup = BeautifulSoup(result.read().decode(), "html.parser")
        name = soup.find(id="product-name").get_text()

        return name
    except:
        return False


@staff_member_required
def discover_barcode(request, barcode):
    """
    Try to guess product details from its barcode
    """
    product = dict()

    product["name"] = product_from_outpan(barcode)
    if product["name"] is False:
        product["name"] = product_from_foodie(barcode)

    if product["name"] is False:
        raise Http404()

    return JsonResponse(product)


@login_required(redirect_field_name=None)
def home(request):
    context = dict(
        money_form=MoneyForm(),
        products=Product.objects.all(),
        categories=Category.objects.all(),
        transactions=request.user.account.transaction_set.all(),
    )

    return render(request, "namubufferiapp/base_home.html", context)


def home_anonymous(request):
    """
    Buying anonymously means that we only update product inventory
    without making transaction for anyone
    """
    context = dict(
        products=Product.objects.all(),
        categories=Category.objects.all(),
    )

    return render(request, "namubufferiapp/base_homeanonymous.html", context)


def buy(request):
    if request.method == "POST":
        try:
            product_key = int(request.POST["product_key"])
        except ValueError:
            # This shouldn't happen, but it did. How?
            payload = {
                "balance": Decimal(0),
                "transactionkey": None,
                "modalMessage": "Tried to buy a product that doesn't exist. How did this happen?",
                "message": render_to_string(
                    "namubufferiapp/message.html",
                    {
                        "message": "Tried to buy a product that doesn't exist. How did this happen?"
                    },
                ),
            }

            mail_admins(
                "Buying without correct product",
                "User {} tried to buy product with id {}".format(
                    request.user, request.POST["product_key"]
                ),
                fail_silently=True,
            )

            return JsonResponse(payload)

        product = get_object_or_404(Product, pk=product_key)
        price = product.price

        new_transaction = Transaction()
        new_transaction.amount = -price
        new_transaction.product = product

        if request.user.is_authenticated:
            new_transaction.customer = request.user.account

        new_transaction.save()
        product.make_sale()

        payload = {
            "balance": Decimal(0),
            "transactionkey": new_transaction.pk,
            "modalMessage": "Purchase Successful",
            "message": render_to_string(
                "namubufferiapp/message.html", {"message": "Purchase Successful"}
            ),
        }

        if request.user.is_authenticated:
            payload["balance"] = request.user.account.balance

            if request.user.account.balance < 0:
                email = EmailMessage(
                    subject="Your balance notification",
                    body="Your balance is NEGATIVE: {}e".format(
                        request.user.account.balance
                    ),
                    to=[request.user.email],
                )

                email.send(fail_silently=True)

        return JsonResponse(payload)
    else:
        raise Http404()


def tos(request):
    if request.method == "POST":
        accept = request.POST["accept"] == "true"

        if request.user.is_authenticated:
            request.user.account.tos_accepted = accept
            request.user.account.save()

    payload = {"tos_accepted": request.user.account.tos_accepted}
    return JsonResponse(payload)


@login_required
def deposit(request):
    if request.method == "POST":
        money_form = MoneyForm(request.POST)

        if money_form.is_valid():
            euros = request.POST["euros"]
            cents = request.POST["cents"]
            amount = Decimal(euros) + Decimal(cents) / 100

            new_transaction = Transaction()
            new_transaction.customer = request.user.account
            new_transaction.amount = amount
            new_transaction.save()

            email = EmailMessage(
                subject="Your balance notification",
                body="Your balance is: {}e".format(request.user.account.balance),
                to=[request.user.email],
            )

            email.send(fail_silently=True)

            return JsonResponse(
                {
                    "balance": request.user.account.balance,
                    "transactionkey": new_transaction.pk,
                    "modalMessage": "Deposit Successful",
                    "message": render_to_string(
                        "namubufferiapp/message.html",
                        {
                            "message": "Deposit Successful",
                            "transaction": new_transaction,
                        },
                    ),
                }
            )
        else:
            return HttpResponseBadRequest(
                '{"errors":' + money_form.errors.as_json() + "}",
                content_type="application/json",
            )
    else:
        raise Http404()


@login_required
def transaction_history(request):
    return JsonResponse(
        {
            "transactionhistory": render_to_string(
                "namubufferiapp/transactionhistory.html",
                {"transactions": request.user.account.transaction_set.all()},
            )
        }
    )


@login_required
def receipt(request):
    if request.method == "POST":
        transaction = get_object_or_404(
            request.user.account.transaction_set.all(),
            pk=request.POST["transaction_key"],
        )

        receipt = {
            "customer": transaction.customer.user.username,
            "amount": transaction.amount,
            "timestamp": transaction.timestamp,
            "transactionkey": transaction.pk,
            "canceled": transaction.canceled,
        }
        try:
            receipt["product"] = transaction.product.name
        except:
            receipt["product"] = "Deposit"

        return JsonResponse({"receipt": receipt})

    else:
        raise Http404()


@login_required
def cancel_transaction(request):
    if request.method == "POST":
        transaction = get_object_or_404(
            request.user.account.transaction_set.all(),
            pk=request.POST["transaction_key"],
        )

        if request.user == transaction.customer.user and not transaction.canceled:
            transaction.cancel()

            return JsonResponse(
                {
                    "balance": request.user.account.balance,
                    "modalMessage": "Transaction Canceled",
                    "message": render_to_string(
                        "namubufferiapp/message.html",
                        {"message": "Transaction Canceled", "transaction": transaction},
                    ),
                }
            )
        else:
            return HttpResponse(status=204)
    else:
        raise Http404()


def magic_auth(request, magic_token=None):
    if request.method == "POST":
        magic_auth_form = MagicAuthForm(request.POST)
        if magic_auth_form.is_valid():
            try:
                user = User.objects.get(
                    email=magic_auth_form.cleaned_data["email"].lower()
                )
            except User.DoesNotExist:
                email = magic_auth_form.cleaned_data["email"].lower()
                m = re.match("^(.*)@aalto.fi$", email)
                if m:
                    username = m.group(1)
                    user = User.objects.create_user(
                        username,
                        email=email,
                        password=b64encode(sha256(urandom(56)).digest()),
                    )
                else:
                    return JsonResponse(
                        {"modalMessage": "Email not found or its not aalto email."}
                    )

            user.account.update_magic_token()

            mail = EmailMultiAlternatives(
                subject="Namubufferi - Login",
                body=(
                    "Hello. Authenticate to Namubufferi using this code. It's valid for 15 minutes.\n"
                    + str(user.account.magic_token)
                ),
                to=[user.email],
            )

            mail.send(fail_silently=True)

            if settings.DEBUG:
                return JsonResponse(
                    {
                        "modalMessage": "<br>login with "
                        + str(user.account.magic_token)
                        + " (Shown when DEBUG)"
                    }
                )
            else:
                return JsonResponse({"modalMessage": "Check your email for the token."})
        else:
            return HttpResponse(
                '{"errors":' + magic_auth_form.errors.as_json() + "}",
                content_type="application/json",
            )

    else:
        user = authenticate(magic_token=str(magic_token))
        if user:
            login(request, user)
            return home(request)
        else:
            return redirect("/")


def tag_auth(request):
    """
    Login by tag
    """
    if request.method == "POST":
        tag_auth_form = TagAuthForm(request.POST)
        if tag_auth_form.is_valid():
            tag_uid = tag_auth_form.cleaned_data["tag_uid"]
            user = authenticate(tagKey=tag_uid)
            if user is not None:
                login(request, user)
                return JsonResponse({"redirect": "/"})
            else:
                return JsonResponse(
                    {
                        "errors": {
                            "tag_uid": [
                                {
                                    "message": "Tag {} not found".format(tag_uid),
                                    "code": "tagnotfound",
                                }
                            ],
                        },
                        "modalMessage": "Tag {} not found!".format(tag_uid),
                    }
                )
        else:
            return HttpResponseBadRequest(
                '{"errors":' + tag_auth_form.errors.as_json() + "}",
                content_type="application/json",
            )
    else:
        raise Http404()


@login_required
def tag_list(request):
    tags = UserTag.objects.filter(user=request.user)

    return JsonResponse(
        {"taglist": render_to_string("namubufferiapp/taglist.html", {"tags": tags})}
    )


@login_required
def tag_modify(request, uid):
    if request.method == "DELETE":
        try:
            tag = UserTag.objects.get(uid=uid)
            if tag.user == request.user:
                tag.delete()
                return HttpResponse("Tag deleted", status=200)
            else:
                raise Http404("Wrong user")
        except UserTag.DoesNotExist:
            raise Http404("Tag does not exist")

    elif request.method == "POST":
        try:
            tag = add_tag_to_user(request.user, uid)
            return HttpResponse("Tag created", status=201)
        except IntegrityError:
            return HttpResponse("Another tag exists ({})!".format(uid), status=409)


def login_view(request):
    return render(
        request,
        "namubufferiapp/base_magiclogin.html",
        context={
            "magic_auth_form": MagicAuthForm(),
            "tag_auth_form": TagAuthForm(),
        },
    )
