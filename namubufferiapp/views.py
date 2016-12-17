import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from forms import MagicLoginForm, MoneyForm
from models import Account, Category, Product, Transaction

from namubufferi import settings


@login_required(redirect_field_name=None)
def home(request):
    return render(
        request,
        "namubufferiapp/base_home.html",
        context={
            "money_form": MoneyForm(),
            "products": Product.objects.all(),
            "categories": Category.objects.all(),
            "transactions": request.user.account.transaction_set.all(),
        },
    )


@login_required
def buy(request):
    if request.user.is_superuser:
        return render(request, "namubufferiapp/base_admin.html")

    if request.method == "POST":
        product = get_object_or_404(Product, pk=request.POST["product_key"])
        price = product.price
        request.user.account.make_payment(price)

        transaction = Transaction.objects.create(
            customer=request.user.account, amount=-price, product=product
        )
        product.make_sale()

        return JsonResponse(
            {
                "balance": request.user.account.balance,
                "transactionkey": transaction.pk,
                "modalMessage": "Purchase Successful",
                "message": render_to_string(
                    "namubufferiapp/message.html", {"message": "Purchase Successful"}
                ),
            }
        )
    else:
        raise Http404()


@login_required
def deposit(request):
    if request.user.is_superuser:
        return render(request, "namubufferiapp/base_admin.html")

    if request.method == "POST":
        form = MoneyForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]
            request.user.account.make_deposit(amount)
            transaaction = Transaction.objects.create(
                customer=request.user.account, amount=amount
            )
            return JsonResponse(
                {
                    "balance": request.user.account.balance,
                    "transactionkey": transaaction.pk,
                    "modalMessage": "Deposit Successful",
                    "message": render_to_string(
                        "namubufferiapp/message.html",
                        {
                            "message": "Deposit Successful",
                            "transaction": transaaction,
                        },
                    ),
                }
            )
        else:
            # https://docs.djangoproject.com/en/1.10/ref/forms/api/#django.forms.Form.errors.as_json
            return JsonResponse({"errors": json.loads(form.errors.as_json())})
    else:
        raise Http404()


@login_required
def transaction_history(request):
    if request.user.is_superuser:
        return render(request, "namubufferiapp/base_admin.html")

    return JsonResponse(
        {
            "transactionhistory": render_to_string(
                "namubufferiapp/transactionhistory.html",
                {"transactions": request.user.account.transaction_set.all()[:5]},
            )
        }
    )


@login_required
def receipt(request):
    if request.user.is_superuser:
        return render(request, "namubufferiapp/base_admin.html")

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
    if request.user.is_superuser:
        return render(request, "namubufferiapp/base_admin.html")

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


def magic_login(request):
    if request.method == "POST":
        form = MagicLoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=request.POST["username"])
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    email=request.POST["username"] + "@aalto.fi",
                    password=None,
                )
                Account.objects.create(
                    user=user,
                )

            user.account.update_magic_token()
            current_site = get_current_site(request)
            magic_link = (
                "http://"
                + current_site.domain
                + reverse(
                    "magic-auth", kwargs={"magic_token": user.account.magic_token}
                )
            )
            context = {"magic_link": magic_link, "subject": "Namubufferi: Magic Link"}
            mail = EmailMultiAlternatives(
                subject="Namubufferi Login",
                body=render_to_string("namubufferiapp/email.txt", context),
                to=[user.email],
            )
            mail.attach_alternative(
                render_to_string("namubufferiapp/email.html", context),
                "text/html",
            )

            mail.send(fail_silently=True)

            if settings.DEBUG:
                return JsonResponse(
                    {"modalMessage": '<a href="' + magic_link + '">Login Link</a>'}
                )
            else:
                return JsonResponse({"modalMessage": "Check your email."})
        else:
            return JsonResponse({"errors": json.loads(form.errors.as_json())})

    return render(
        request,
        template_name="namubufferiapp/base_magiclogin.html",
        context={
            "form": MagicLoginForm(),
        },
    )


def magic_auth(request, magic_token=None):
    user = authenticate(magic_token=magic_token)
    if user:
        login(request, user)
        return redirect("home")
    else:
        return HttpResponse(status=403)
