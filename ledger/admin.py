from django.contrib import admin
from .models import Product, Transaction, MobilePayTransaction

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'hidden', 'tag_list')
    list_filter = ('hidden', 'tags')
    search_fields = ['name']

    # Django-Taggit: https://django-taggit.readthedocs.io/en/latest/admin.html
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'concept', 'amount', 'timestamp')
    ordering = ('-timestamp',)
    search_fields = ['user__username', 'concept', 'timestamp', 'amount']

    def user_name(self, obj):
        return obj.user.username
    
    def product_name(self, obj):
        if obj.product:
            return obj.product.name
        else:
            return None
        
    def has_change_permission(self, request, obj=None):
        return False

class MobilePayTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reference', 'timestamp')
    list_filter = ('amount',)
    search_fields = ['user__username', 'reference', 'timestamp', 'amount']
    ordering = ('-timestamp',)
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(MobilePayTransaction, MobilePayTransactionAdmin)