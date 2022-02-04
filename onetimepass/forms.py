from django import forms

from .models import OneTimePass


class OneTimePassCheckForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "one-time-code",
                "autofocus": True,
                "placeholder": "One-time password",
            }
        )
    )


class OneTimePassForm(forms.ModelForm):
    class Meta:
        model = OneTimePass
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "autofocus": True,
                    "placeholder": "email",
                }
            )
        }
