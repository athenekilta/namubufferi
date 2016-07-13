from django.contrib import admin

# Register your models here.
from .models import Category, Product, Transaction, Payment, Deposit, TransactionAdmin

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Deposit)
admin.site.register(Transaction, TransactionAdmin)
