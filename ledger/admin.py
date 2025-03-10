
import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime
from django.utils.dateparse import parse_datetime
from .models import Account, Barcode, Group, Product, Transaction
from .models import Product  # Importtaa kaikki valikoiman tuotteet
import logging

logger = logging.getLogger(__name__)

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
    list_display = ("name", "price", "inventory", "hidden")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "account", "product", "price", "quantity", "total")
    list_filter = (("timestamp", DateRangeFilterBuilder()),)

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        current_date = timezone.now().strftime("%Y-%m-%d")
        field_names = ['Product', 'Quantity sold', 'Sales (EUR)']

        # Extract date range from request GET parameters
        start_date = request.GET.get('timestamp__range__gte')
        end_date = request.GET.get('timestamp__range__lte')
        if start_date and end_date:
            start_date_str = start_date.split('T')[0]  # Extract date part
            end_date_str = end_date.split('T')[0]  # Extract date part

            # Check if end date is in the future
            if datetime.strptime(end_date_str, "%Y-%m-%d") > datetime.strptime(current_date, "%Y-%m-%d"):
                end_date_str = current_date

            date_range = f"{start_date_str}_to_{end_date_str}"
        else:
            date_range = current_date  # replace with today, if end date is in the future

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename=namubufferi-report-{date_range}.csv' # filename contains date range
        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(field_names)

        product_counts = {product.name: {'quantity': 0, 'sales': 0} for product in Product.objects.filter(price__gt=0)}
        total_sales = 0
        for obj in queryset:
            # Only take positive prices
            if obj.price >= 0:
                product_name = obj.product.name
                product_counts[product_name]['quantity'] += obj.quantity * -1
                product_counts[product_name]['sales'] += obj.quantity * obj.price / -100  # Convert cents to euros
                total_sales += obj.quantity * obj.price / -100  # Convert cents to euros

        for product_name, data in product_counts.items():
                writer.writerow([product_name, data['quantity'], f"{data['sales']:.2f}".replace('.', ',')])  # decimal separator is comma

        writer.writerow(['Total', '', f"{total_sales:.2f}".replace('.', ',')])  # decimal separator is comma

        return response

    export_as_csv.short_description = _("Export selected transactions") 


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "is_staff", "is_superuser", "last_login", "balance")
    list_filter = UserAdmin.list_filter + (BalanceListFilter,)

    def balance(self, instance):
        return instance.account.balance
