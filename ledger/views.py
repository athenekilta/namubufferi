from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Ingress, TransferSend, TransferReceive, Purchase
from .forms import FundsForm, BuyForm, TransferForm
from django.utils.translation import gettext_lazy as _

class AllTransactionsView(ListView):
    '''
    Show all users transactions.
    '''
    template_name = "ledger/all_my_transactions.html"
    context_object_name = "all_transactions_list"
    login_url = reverse_lazy('login')
    paginate_by = 20
    
    def get_queryset(self):
        '''
        Return all transactions for the user.
        '''
        transactions = []
        transactions.extend(Ingress.objects.filter(user=self.request.user))
        transactions.extend(TransferSend.objects.filter(user=self.request.user))
        transactions.extend(TransferReceive.objects.filter(user=self.request.user))
        transactions.extend(Purchase.objects.filter(user=self.request.user))
        return sorted(transactions, key=lambda x: x.timestamp, reverse=True)
    
class BuyView(FormView):
    template_name = 'ledger/buy.html'
    form_class = BuyForm
    success_url = reverse_lazy('ledger:buy')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Successful purchase! Enjoy it! 🥳🍰'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('There was an error with your submission. Please try again. 🚧'))
        return super().form_invalid(form)

class TransferView(FormView):
    """
    Transfer money to another user form.
    """
    template_name = 'ledger/transfer.html'
    form_class = TransferForm
    success_url = reverse_lazy('ledger:buy')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Transfer successful! 😔➡️😁"))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _('There was an error with your submission. Please try again. 🚧'))
        return super().form_invalid(form)

class FundsView(FormView):
    """
    Add funds to your account form. Add funds by checking the transaction id in MobilePay.
    """
    template_name = 'ledger/funds.html'
    form_class = FundsForm
    success_url = reverse_lazy('ledger:buy')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Funds added successfully! 🥳💰')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('There was an error with your submission. Please try again. 🚧'))
        return super().form_invalid(form)