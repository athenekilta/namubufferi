from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import identify_hasher, make_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from uuidmodels.models import UUIDModel


def onetimepass_email_validator(value):
    EmailValidator()(value)
    if "*" in settings.ONETIMEPASS_ALLOWED_DOMAINS:
        return
    if value.split("@")[1] not in settings.ONETIMEPASS_ALLOWED_DOMAINS:
        raise ValidationError("Domain not allowed")


class OneTimePass(UUIDModel):
    email = models.EmailField(validators=[onetimepass_email_validator])
    password = models.CharField(max_length=128)
    time_to_live = models.PositiveSmallIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    attempts = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "one-time password"

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_check_url(self):
        return reverse("onetimepass:check", kwargs={"pk": self.pk})

    @property
    def expires(self):
        return self.created_at + timedelta(minutes=self.time_to_live)

    @property
    def is_alive(self):
        return timezone.now() < self.expires

    @property
    def retry_after(self):
        return int((self.expires - timezone.now()).total_seconds())

    @property
    def is_rate_limited(self):
        return self.attempts > 2
