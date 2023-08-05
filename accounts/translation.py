from modeltranslation.translator import register, TranslationOptions
from .models import TermsOfService, PrivacyPolicy

@register(TermsOfService)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'content', )

@register(PrivacyPolicy)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'content', )