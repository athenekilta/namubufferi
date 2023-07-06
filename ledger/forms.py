from django import forms


class FundsForm(forms.Form):
    id = forms.CharField(label="Transaction ID", max_length=100)