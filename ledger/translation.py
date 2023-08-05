from modeltranslation.translator import register, TranslationOptions
from .models import Product, ProductTag

@register(ProductTag)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)