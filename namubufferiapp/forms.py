from django import forms


class MoneyForm(forms.Form):
    amount = forms.DecimalField(max_digits=6, decimal_places=1)
