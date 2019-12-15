from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Account, UserTag


class MagicAuthBackend(object):
    """
    https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#authentication-backends
    """

    def authenticate(self, magic_token=None):
        try:
            account = Account.objects.get(magic_token=magic_token.upper())
        except:
            return None
        if account.magic_token_is_alive():
            account.deactivate_magic_token()
            return account.user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def add_tag_to_user(user, tagKey):
    oldTags = UserTag.objects.all()
    for oldTag in oldTags:
        if check_password(tagKey, oldTag.uid):
            raise IntegrityError

    tagHash = make_password(tagKey)

    tag = UserTag.objects.create(user=user, uid=tagHash)
    tag.save()

    return tag


class TagAuthBackend(ModelBackend):
    """
    Authenticate with NFC tag.
    """

    def authenticate(self, tagKey=None):
        tags = UserTag.objects.all()
        for tag in tags:
            if check_password(tagKey, tag.uid):
                return tag.user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
