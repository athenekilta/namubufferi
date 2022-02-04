from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Document, Terms


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_terms(sender, instance, created, **kwargs):
    if not Document.objects.exists():
        Document.objects.create(text="Lorem ipsum")
    if created:
        Terms.objects.create(user=instance, document=Document.objects.first())
