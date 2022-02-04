from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from .models import Keycard

User = get_user_model()

# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#authentication-backends


class KeycardBackend(BaseBackend):
    def authenticate(self, request, secret=None):
        for keycard in Keycard.objects.all():
            if check_password(secret, keycard.secret):
                return keycard.user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
