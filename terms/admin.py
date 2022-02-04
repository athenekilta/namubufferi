from django.contrib import admin

from .models import Document, Terms


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    list_display = ("user", "accepted")
