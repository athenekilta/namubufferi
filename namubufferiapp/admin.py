from django.contrib import admin

# Register your models here.
from .models import Category, Product, Transaction, UserTag

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(UserTag)
