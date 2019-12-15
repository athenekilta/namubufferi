from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Account, Category, Product, ProductTag, Transaction, UserTag


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = "Account"
    fk_name = "user"


class BalanceListFilter(admin.SimpleListFilter):
    title = "balance"
    parameter_name = "balance"
    default_value = None

    def lookups(self, request, model_admin):
        return [("negative", "negative balances only")]

    def queryset(self, request, queryset):
        if self.value() == "negative":
            negative_users = []
            for user in queryset:
                if user.account.balance < 0:
                    negative_users.append(user.id)
            return User.objects.filter(id__in=negative_users)

        return queryset


class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline,)
    list_display = ("email", "is_staff", "is_superuser", "last_login", "balance")
    list_select_related = ("account",)
    list_filter = UserAdmin.list_filter + (BalanceListFilter,)

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
