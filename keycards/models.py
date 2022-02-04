from django.conf import settings
from django.contrib.auth.hashers import check_password, identify_hasher, make_password
from django.core.exceptions import ValidationError
from django.db import models

from uuidmodels.models import UUIDModel


class Keycard(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.CharField(max_length=128, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.timestamp}"

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.secret)
        except ValueError:
            self.secret = make_password(self.secret)
        super().save(*args, **kwargs)

    def clean(self):
        for keycard in Keycard.objects.all():
            if check_password(self.secret, keycard.secret):
                raise ValidationError("Secret already added")
        return super().clean()
