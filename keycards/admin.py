from django.contrib import admin

from .models import Keycard


@admin.register(Keycard)
class KeycardAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user")
