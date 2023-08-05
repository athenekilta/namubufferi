from django.contrib import admin
from .models import Product, Purchase, TransferSend, TransferReceive, Ingress, ProductTag
from modeltranslation.admin import TabbedTranslationAdmin
from taggit.models import Tag

class ProductTagAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name']

class ProductAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'price', 'tag_list')
    list_filter = ('tags',)
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
    


admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, TransactionAdmin)
admin.site.register(TransferSend, TransactionAdmin)
admin.site.register(TransferReceive, TransactionAdmin)
admin.site.register(Ingress, TransactionAdmin)
admin.site.unregister(Tag)
admin.site.register(ProductTag, ProductTagAdmin)