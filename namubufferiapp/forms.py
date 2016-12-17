from django import forms
from django.core.validators import RegexValidator


class MoneyForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "step": "0.05",
                "autofocus": "",
            }
        ),
    )


class MagicLoginForm(forms.Form):
    username = forms.CharField(
        validators=[RegexValidator(r"(^[a-zA-Z0-9_.+-]*$)", "Enter a valid email.")],
        widget=forms.TextInput(
            attrs={
                "placeholder": "teemu.teekkari",
                "class": "form-control",
            }
        ),
    )
