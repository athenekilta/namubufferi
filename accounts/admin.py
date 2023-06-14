
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, PassPhrase

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('date_joined', 'last_login')
    list_display = (
        'username', 'email', 'is_staff', 'balance'
        )
    
    fieldsets = (
        ('Additional info', {
            'fields': ('balance',)
        }),
        ('Credentials', {
            'fields': ('username', 'email', 'password')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )


    add_fieldsets = (
        ('Additional info', {
            'fields': ('balance',)
        }),
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
    )


@admin.register(PassPhrase)
class PassPhraseAdmin(admin.ModelAdmin):
    list_display = ('passphrase',)
    fields = ('passphrase',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False