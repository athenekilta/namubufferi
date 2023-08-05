from django import forms
from .models import Product, Purchase, TransferSend, ProductTag
from accounts.models import CustomUser as User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .funds_logic import retrieve_transaction, create_transaction, check_transaction, ERROR_CODES

class BuyForm(forms.Form):
    products = Product.objects.all()
    tags = ProductTag.objects.all()
    product = forms.ModelChoiceField(
        queryset=products,
        widget=forms.RadioSelect,
        empty_label=None,  # This will force the user to select a product
        label=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BuyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        selected_product = cleaned_data.get('product')
        if selected_product and self.user.balance < selected_product.price:
            raise forms.ValidationError(_("Insufficient funds"))
        return cleaned_data
    
    def save(self):
        selected_product = self.cleaned_data['product']
        Purchase.objects.create(
            user=self.user,
            product=selected_product,
            amount=selected_product.price
        )

class TransferForm(forms.Form):
    username = forms.CharField(max_length=100, label=_("Username"), help_text=_("Enter the username of the user you want to transfer funds to."))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label=_("Amount to transfer"), help_text=_("Enter the amount of funds you want to transfer."))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TransferForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        """
        Check that the username exists.
        """
        username = self.cleaned_data['username']
        User = get_user_model()
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(_("User does not exist"))
        return username
    
    def clean_amount(self):
        """
        Check that the amount is greater than 0.
        """
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError(_("Amount must be greater than 0"))
        return amount

    def clean(self):
        """
        Check that user has enough funds.
        """
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        if amount and self.user.balance < amount:
            raise forms.ValidationError(_("Insufficient funds"))
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        amount = self.cleaned_data['amount']
        recipient = User.objects.get(username=username)
        TransferSend.objects.create(
            user=self.user,
            amount=amount,
            recipient_user=recipient
        )

class FundsForm(forms.Form):
    id = forms.CharField(label=_("Transaction ID"), max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FundsForm, self).__init__(*args, **kwargs)
        if self.errors:
            self.fields['id'].widget.attrs['value'] = self.data.get('id')

    def clean_id(self):
        transaction_id = self.cleaned_data['id']
        response = retrieve_transaction(transaction_id)
        if response.status_code == 200:
            transaction = response.json()
            error_code = check_transaction(transaction)
            if error_code == 0:
                self.transaction = transaction
                return transaction
            else:
                raise forms.ValidationError(_(ERROR_CODES[error_code]))
        else:
            raise forms.ValidationError(_("Transaction not found"))

    def save(self):
        create_transaction(self.transaction, self.user)