import uuid

from django.db import models


class UUIDModel(models.Model):
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#uuidfield
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
