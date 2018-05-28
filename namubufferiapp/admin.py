from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Category, Product, Transaction, UserTag, ProductTag, Account


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Account'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline, )
    list_display = ('email', 'is_staff', 'is_superuser', 'last_login', 'balance')
    list_select_related = ('account', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def balance(self, instance):
        return instance.account.balance

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(UserTag)
admin.site.register(ProductTag)
