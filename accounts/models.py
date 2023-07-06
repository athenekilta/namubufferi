from django.db import models
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist

class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class PassPhrase(models.Model):
    passphrase = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get(pk=1)
        except ObjectDoesNotExist:
            return cls()
        
    def __str__(self):
        return self.passphrase if self.passphrase else "No passphrase set"
    
    class Meta:
        verbose_name = "Passphrase"
        verbose_name_plural = "Passphrase"