from django import forms
from accounts.mails import send_activation_email, send_password_reset_email
from .models import CustomUser as User, PassPhrase
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    passphrase = forms.CharField(max_length=100, required=False)
    accept_terms = forms.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.errors:
            self.fields['email'].widget.attrs['value'] = self.data.get('email')
            self.fields['username'].widget.attrs['value'] = self.data.get('username')
            self.fields['password1'].widget.attrs['value'] = self.data.get('password1')
            self.fields['password2'].widget.attrs['value'] = self.data.get('password2')
            self.fields['passphrase'].widget.attrs['value'] = self.data.get('passphrase')
            self.fields['accept_terms'].widget.attrs['value'] = self.data.get('accept_terms')

    def clean_passphrase(self):
        passphrase = self.cleaned_data.get('passphrase')
        if passphrase:
            correct_passphrase = PassPhrase.objects.first()
            if not correct_passphrase or passphrase != correct_passphrase.passphrase:
                raise forms.ValidationError('Passphrase does not match!')
        return passphrase
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Mail already exists."))
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("Username already exists."))
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
            send_activation_email(user, self.request)
        return user

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label=_("Username"), help_text=_("Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."))
    email = forms.EmailField(required=True, label=_("Email"), help_text=_("Required. 254 characters or fewer."))
    language = forms.ChoiceField(choices=settings.LANGUAGES, widget=forms.Select(), required=True, label=_("Language"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['language'].initial = self.user.language
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() and username != self.user.username:
            raise ValidationError(_("Username already exists."))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and email != self.user.email:
            raise ValidationError(_("Mail already exists."))
        return email

    def save(self, commit=True):
        self.user.username = self.cleaned_data.get('username')
        self.user.email = self.cleaned_data.get('email')
        self.user.language = self.cleaned_data.get('language')

        if commit:
            self.user.save()
        return self.user

    class Meta:
        model = User
        fields = ('username', 'email', 'language',)

class ProfileChangePasswordForm(forms.Form):
    """
    Form for changing user password.
    """
    old_password = forms.CharField(max_length=100, required=True, label=_("Old password"), widget=forms.PasswordInput())
    new_password1 = forms.CharField(max_length=100, required=True, label=_("New password"), widget=forms.PasswordInput())
    new_password2 = forms.CharField(max_length=100, required=True, label=_("New password confirmation"), widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError(_("Wrong password."))
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise ValidationError(_("Passwords doesn't match."))
        return new_password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data.get('new_password1'))
        if commit:
            self.user.save()
        return self.user
    
class ProfileDeleteForm(forms.Form):
    """
    Form for deleting user profile.
    """
    password = forms.CharField(max_length=100, required=True, label=_("Password"), widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileDeleteForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise ValidationError(_("Wrong password."))
        return password

    def save(self, commit=True):
        self.user.delete()
        return self.user

class PasswordResetForm(forms.Form):
    """
    Form for resetting user password.
    """
    email = forms.EmailField(required=True, label=_("Email"), help_text=_("Required. 254 characters or fewer."))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("El email no existe."))
        return email

    def save(self, commit=True):
        user = User.objects.get(email=self.cleaned_data.get('email'))
        if commit:
            send_password_reset_email(user, self.request)
        return user