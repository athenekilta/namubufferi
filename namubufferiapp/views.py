from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from forms import MoneyForm, MagicAuthForm
from models import Account, Product, Category, Transaction
from namubufferi.settings import DEBUG


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


@login_required
def buy(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=request.POST['product_key'])
        price = product.price
        request.user.account.make_payment(price)

        new_transaction = Transaction()
        new_transaction.customer = request.user.account
        new_transaction.amount = -price
        new_transaction.product = product
        new_transaction.save()

        product.make_sale()

        return JsonResponse({'balance': request.user.account.balance,
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


def register(request):
    """
    https://docs.djangoproject.com/en/1.10/topics/email/
    """

    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            print request.POST
            new_user = register_form.save()

            new_account = Account()
            new_account.user = new_user
            new_account.save()

            return JsonResponse({'modalMessage': "Register Success. You can now sign in.",
                                 'message': render_to_string('namubufferiapp/message.html',
                                                             {'message': "Register Success. You can now sign in."})
                                 })
        else:
            return HttpResponse('{"errors":' + register_form.errors.as_json() + '}', content_type="application/json")

    else:
        raise Http404()


def magic_auth(request, magic_token=None):
    """
    """
    if request.method == 'POST':

        # Validate form
        magic_auth_form = MagicAuthForm(request.POST)
        if magic_auth_form.is_valid():
            # Try to find the user or create a new one
            try:
                user = User.objects.get(username=request.POST['aalto_username'])
            except:  # DoesNotExist
                new_user = User.objects.create_user(request.POST['aalto_username'],
                                                    email=request.POST['aalto_username'] + '@aalto.fi',
                                                    password=None)

                new_account = Account()
                new_account.user = new_user
                new_account.save()
                user = new_user

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
                print "Mail sent"
            except:
                print "Mail not sent"

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
