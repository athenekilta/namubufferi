from django import forms
from django.core.validators import RegexValidator


class MoneyForm(forms.Form):
    #amount = forms.DecimalField(max_digits=5, decimal_places=1, widget=forms.NumberInput(attrs={'pattern': '[0-9]*'}))
    euros = forms.IntegerField(min_value=0,
                               max_value=100,
                               widget=forms.NumberInput(attrs={'pattern': '[0-9]*',
                                                               'class': 'form-control',
                                                               'placeholder': '00',
                                                               'autofocus': '',
                                                               'value': '00',
                                                               }))
    cents = forms.IntegerField(min_value=0,
                               max_value=95,
                               widget=forms.NumberInput(attrs={'pattern': '[0-9]*',
                                                               'class': 'form-control',
                                                               'step': '5',
                                                               'placeholder': '00',
                                                               'value': '00',
                                                               }))


class MagicAuthForm(forms.Form):
    # http://emailregex.com/
    emailregex = RegexValidator(r"(^[a-zA-Z0-9_.+-]*$)", 'Enter a valid email.')

    aalto_username = forms.CharField(label='Username',
                                     validators=[emailregex],
                                     widget=forms.TextInput(attrs={'placeholder': 'teemu.teekkari',
                                                                   'class': 'form-control',
                                                                   }))

class TagAuthForm(forms.Form):
    tag_uid = forms.CharField(label='NFC-tag',
                              widget=forms.TextInput(attrs={'placeholder': '123A4F5C',
                                                            'class': 'form-control',
                                                            }))
