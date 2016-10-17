# Namubufferi magic link authentication backend
from django.utils import timezone
from django.contrib.auth.models import User

from models import UserProfile


class MagicAuthBackend(object):
    """
    https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#authentication-backends
    """
    def authenticate(self, magic_token=None):
        # Check the token and return a User.
        try:
            user_profile = UserProfile.objects.get(magic_token=magic_token)
        except:
            return None
        if user_profile.magic_token_is_alive():
            user_profile.deactivate_magic_token()
            return user_profile.user
        else:
            return None

    def get_user(self, user_id):
        # Not sure what this is for
        # http://stackoverflow.com/questions/13954309/custom-authentification-backend-django?answertab=votes#tab-top
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
