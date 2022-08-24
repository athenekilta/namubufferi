from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import Form, PasswordInput, ModelForm
from django.forms import fields


User = get_user_model()


class InputSecretForm(Form):
    secret = fields.CharField(
        widget=PasswordInput(), 
        help_text='This should be visible in olkkari'
    )

    def clean_secret(self):
        input = self.cleaned_data['secret']

        print(input)
        print(settings.SIGNUP_SECRET)

        if input != settings.SIGNUP_SECRET:
            raise ValidationError('Incorrect Secret!')

class ClaimBalanceForm(InputSecretForm):
    name_in_namubuffa = fields.CharField()
    email = fields.EmailField()


class CreateUserForm(UserCreationForm, InputSecretForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ManageUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'alias']