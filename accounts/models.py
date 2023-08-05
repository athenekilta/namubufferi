from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    email = models.EmailField(unique=True)
    language = models.CharField(
        max_length=5,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        verbose_name=_('Language')
    )

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
        return self.passphrase if self.passphrase else _("No passphrase set")
    
    class Meta:
        verbose_name = _("Passphrase")
        verbose_name_plural = _("Passphrase")

class TermsOfService(models.Model):
    """
    Terms of service for the application.
    """
    title = models.CharField(max_length=128, blank=False)
    content = models.TextField(blank=False)

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
        return self.title if self.title else _("No terms set")
    
    class Meta:
        verbose_name_plural = _("Terms of service")
        verbose_name = _("Term of service")
        ordering = ["title"]

class PrivacyPolicy(models.Model):
    """
    Privacy policy for the application.
    """
    title = models.CharField(max_length=128, blank=False)
    content = models.TextField(blank=False)

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
        return self.title if self.title else _("No terms set")
    
    class Meta:
        verbose_name_plural = _("Privacy policies")
        verbose_name = _("Privacy policy")
        ordering = ["title"]
