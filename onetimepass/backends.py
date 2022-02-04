from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from .models import OneTimePass

User = get_user_model()

# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#authentication-backends


class OneTimePassBackend(BaseBackend):
    def authenticate(self, request, onetimepass_id=None, password=None):
        try:
            onetimepass = OneTimePass.objects.get(id=onetimepass_id)
        except OneTimePass.DoesNotExist:
            return None
        if onetimepass.password is None or password is None:
            return None
        if (
            check_password(password, onetimepass.password)
            and onetimepass.is_alive
            and not onetimepass.is_rate_limited
        ):
            try:
                user = User.objects.get(email=onetimepass.email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=onetimepass.email, email=onetimepass.email, password=None
                )
            onetimepass.delete()
            return user
        onetimepass.attempts += 1
        onetimepass.save()
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
