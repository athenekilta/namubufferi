from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import CustomUser, PassPhrase, TermsOfService, PrivacyPolicy

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

@admin.register(TermsOfService)
class TermsOfServiceAdmin(TabbedTranslationAdmin):
    list_display = ('title',)
    fields = ('title', 'content',)

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(TabbedTranslationAdmin):
    list_display = ('title',)
    fields = ('title', 'content',)
