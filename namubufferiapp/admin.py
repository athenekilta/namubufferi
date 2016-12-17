from django.contrib import admin

from .models import Category, Product, Transaction

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Transaction)
