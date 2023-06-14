from django import forms
from .models import CustomUser, PassPhrase
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    accept_terms = forms.BooleanField(required=True)
    passphrase = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.errors:
            self.fields['email'].widget.attrs['value'] = self.data.get('email')
            self.fields['username'].widget.attrs['value'] = self.data.get('username')
            self.fields['password1'].widget.attrs['value'] = self.data.get('password1')
            self.fields['password2'].widget.attrs['value'] = self.data.get('password2')
            self.fields['accept_terms'].widget.attrs['value'] = self.data.get('accept_terms')
            self.fields['passphrase'].widget.attrs['value'] = self.data.get('passphrase')

    def clean(self):
        cleaned_data = super().clean()
        passphrase = PassPhrase.objects.first().passphrase
        if passphrase and cleaned_data.get('passphrase') != passphrase:
            raise forms.ValidationError('Passphrase does not match!')
        if passphrase is None and not cleaned_data.get('passphrase') == '':
            raise forms.ValidationError('Passphrase does not match!')
        return cleaned_data