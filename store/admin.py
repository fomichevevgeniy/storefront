from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import *

# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    # Как выглядят кнопки фильтра
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    # Как реагировать на нажатие кнопок фильтра
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)  # Меньше чем 10


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" width="75">')
        return ''

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']  # Поле slug будет заполняться на основе title
        # Пылесос -> pilesos  iphone-15-pro-max
    }
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price', 'inventory_status',
                    'collection']
    list_editable = ['unit_price']
    list_per_page = 10  # 10 шт за страницу
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
            'collection__id': str(collection.id)
            # admin:store_product_changelist?collection__id=1
        })
        )
        return format_html(f'<a href="{url}">{collection.products_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )