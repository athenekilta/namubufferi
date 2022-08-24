from django.contrib.auth.models import AbstractUser
from django.db import models

from uuidmodels.models import UUIDModel


class User(AbstractUser, UUIDModel):
    alias = models.CharField(max_length=64, null=True, unique=True)

    def get_alias(self):
        return self.alias or self.username
