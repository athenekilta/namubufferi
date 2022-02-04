from django.contrib.auth.models import AbstractUser

from uuidmodels.models import UUIDModel


class User(AbstractUser, UUIDModel):
    pass
