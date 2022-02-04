from django.contrib import admin

from .models import OneTimePass


@admin.register(OneTimePass)
class OneTimePassAdmin(admin.ModelAdmin):
    list_display = ("email", "expires")
