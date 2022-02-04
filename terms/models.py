from django.conf import settings
from django.db import models


class Document(models.Model):
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:64]}"


class Terms(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.PROTECT)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "terms"

    def __str__(self):
        return f"{self.user}"
