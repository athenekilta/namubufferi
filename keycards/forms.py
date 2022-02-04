from django import forms


class KeycardLoginForm(forms.Form):
    secret = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "autofocus": True,
            }
        )
    )
