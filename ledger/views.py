from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from accounts.models import CustomUser as User
from taggit.models import Tag
from rest_framework.generics import ListAPIView

from django.conf import settings
import stripe

from .models import Transaction, Product
from .serializers import ProductSerializer

from django.urls import reverse_lazy

class IndexView(LoginRequiredMixin, ListView):
    '''
    Show the last 5 transactions.
    '''
    template_name = "ledger/index.html"
    context_object_name = "latest_transactions_list"
    login_url = '/accounts/login'

    def get_queryset(self):
        '''
        Return the last 5 transactions.
        '''
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by("-timestamp")[:5]

    def get_context_data(self, **kwargs):
        '''
        Add the user object to the context
        '''
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class AllTransactionsView(LoginRequiredMixin, ListView):
    '''
    Show all users transactions.
    '''
    template_name = "ledger/all_my_transactions.html"
    context_object_name = "all_transactions_list"
    login_url = reverse_lazy('login')
    paginate_by = 10
    def get_queryset(self):
        '''
        Return all transactions for the user.
        '''
        return Transaction.objects.filter(user=self.request.user).order_by("-timestamp")
    
class BuyProductView(LoginRequiredMixin, ListView):
    '''
    Show all the Product groups and the products.
    '''
    template_name = "ledger/buy_product.html"
    context_object_name = "product_list"
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        '''
        Return all products grouped by tag.
        '''
        product_list = Product.objects.filter(hidden=False).prefetch_related('tags').all()
        tags = Tag.objects.all()
        context = {
            'product_list': product_list,
            'tags': tags,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        '''
        Handle the POST request for buying a product.
        '''
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        Transaction.objects.create(
                                    user=request.user,
                                    product=product, 
                                    amount=product.price * -1
                                )
        return redirect('ledger:index')
    
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class TransferView(LoginRequiredMixin, ListView):
    '''
    Transfer money to another user or add it using MobilePay, Stripe or Paypal.
    '''
    template_name = "ledger/transfer.html"
    context_object_name = "user_list"
    login_url = reverse_lazy('login')
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        '''
        Handle the POST request for transferring money.
        '''
        recipient_name = request.POST.get('recipient')
        recipient = User.objects.get(username=recipient_name)
        amount = int(request.POST.get('amount'))
        Transaction.objects.create(
            user=request.user,
            amount=amount,
            recipient_user=recipient
        )
        return redirect('ledger:index')


class AddFundsView(LoginRequiredMixin, ListView):
    """
    Add funds to the user's account.
    """
    template_name = "ledger/add_funds.html"
    login_url = reverse_lazy('login')
    context_object_name = "available_payment_methods"

    def get_queryset(self):
        '''
        Return the available payment methods.
        '''
        available_payment_methods = []
        if hasattr(settings, 'STRIPE_PUBLISHABLE_KEY') \
             and hasattr(settings, 'STRIPE_SECRET_KEY'):
            available_payment_methods.append('stripe')
        if hasattr(settings, 'MOBILEPAY_MERCHANT_ID'):
            available_payment_methods.append('mobilepay')

        return available_payment_methods

    def post(self, request, *args, **kwargs):
        '''
        Handle the POST request for adding funds.
        '''
        amount = int(request.POST.get('amount'))
        payment_method = request.POST.get('payment-method')
        return redirect('ledger:add')
