from django import forms
from django.core.validators import RegexValidator
from .models import Product, Category

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
    emailregex = RegexValidator(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", 'Enter a valid email.')

    email = forms.CharField(label='Email',
                            validators=[emailregex],
                            widget=forms.TextInput(attrs={'placeholder': 'teemu.teekkari@aalto.fi',
                                                           'class': 'form-control',
                                                           'autocomplete': 'off',
                                                           'autocapitalize': 'none',
                                                           }))

class TagAuthForm(forms.Form):
    tag_uid = forms.CharField(label='NFC-tag',
                              widget=forms.TextInput(attrs={'placeholder': '123A4F5C',
                                                            'class': 'form-control',
                                                            'autocomplete': 'off',
                                                            'autocapitalize': 'none',
                                                            }))

class ProductForm(forms.Form):
    name = forms.CharField(label='Product name',
                            widget=forms.TextInput(attrs={'class': 'form-control',}))
    price = forms.DecimalField(label='Product price',
                            widget=forms.NumberInput(attrs={'class': 'form-control',}))
    inventory = forms.IntegerField(label='Product stock count',
                            widget=forms.NumberInput(attrs={'class': 'form-control',}))
    hidden = forms.BooleanField(label='Is product hidden?',
                            required=False,
                            widget=forms.CheckboxInput())
    category = forms.ModelChoiceField(label='Product category',
                            queryset=Category.objects.all(),
                            widget=forms.Select(attrs={'class': 'form-control',}))
    barcode = forms.CharField(label='Product barcode',
                            required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control',}))
