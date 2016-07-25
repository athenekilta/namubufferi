from django import forms


class MoneyForm(forms.Form):
    #amount = forms.DecimalField(max_digits=5, decimal_places=1, widget=forms.NumberInput(attrs={'pattern': '[0-9]*'}))
    euros = forms.IntegerField(min_value=0, max_value=100, widget=forms.NumberInput(attrs={'pattern': '[0-9]*', 'class': 'form-control', 'placeholder': '00', 'autofocus':''}))
    cents = forms.IntegerField(min_value=0, max_value=95, widget=forms.NumberInput(attrs={'pattern': '[0-9]*', 'class': 'form-control', 'step': '5', 'placeholder': '00'}))
