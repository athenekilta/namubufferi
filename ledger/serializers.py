from rest_framework import serializers
from taggit.serializers import (
    TagListSerializerField,
    TaggitSerializer,
)

from ledger.models import Product

class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'tags')