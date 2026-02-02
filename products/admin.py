from django.contrib import admin
from .models import Store, Product, PriceHistory


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'store',
                    'url',
                    'target_price',
                    'current_price', 
                    'user',
                    'created_at',
                    'update_at'
                    ]
    list_filter = ['store', 'user']
    search_fields = ['name', 'url']
    readonly_fields = ['created_at', 'update_at']
    list_per_page = 20



@admin.register(PriceHistory)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name']
    date_hierarchy = 'created_at'
