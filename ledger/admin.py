from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Account, Barcode, Group, Product, Transaction


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

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        date = timezone.now().strftime("%Y-%m-%d")
        field_names = ['Product', 'Quantity', 'Sales (€)']

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename=namubufferi-report-{date}.csv'
        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(field_names)

        product_counts = {}
        total_sales = 0
        for obj in queryset:
            product_name = obj.product.name
            if product_name in product_counts:
                product_counts[product_name]['quantity'] += obj.quantity
                product_counts[product_name]['sales'] += obj.quantity * obj.price / 100  # Convert cents to euros
            else:
                product_counts[product_name] = {
                    'quantity': obj.quantity,
                    'sales': obj.quantity * obj.price / 100  # Convert cents to euros
                }
            total_sales += obj.quantity * obj.price / 100  # Convert cents to euros

        for product_name, data in product_counts.items():
            writer.writerow([product_name, data['quantity'], data['sales']])

        writer.writerow(['Total', '', total_sales])

        return response

    export_as_csv.short_description = _("Export Selected")




@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "is_staff", "is_superuser", "last_login", "balance")
    list_filter = UserAdmin.list_filter + (BalanceListFilter,)

    def balance(self, instance):
        return instance.account.balance
