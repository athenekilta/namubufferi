from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from rangefilter.filters import (
    DateRangeFilterBuilder,
)

from .models import Account, Barcode, Group, Product, Transaction

User = get_user_model()


class BalanceListFilter(admin.SimpleListFilter):
    title = "balance"
    parameter_name = "balance"

    def lookups(self, request, model_admin):
        return (("negative", "Negative balances only"),)

    def queryset(self, request, queryset):
        if self.value() == "negative":
            return queryset.filter(
                pk__in=(user.pk for user in queryset if user.account.balance < 0)
            )
        return queryset


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ("id", "product")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ("products",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "inventory")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "account", "product", "price", "quantity", "total")
    list_filter = (("timestamp", DateRangeFilterBuilder()),)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "is_staff", "is_superuser", "last_login", "balance")
    list_filter = UserAdmin.list_filter + (BalanceListFilter,)

    def balance(self, instance):
        return instance.account.balance
