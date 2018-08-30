from django.contrib import admin

# Register your models here.
from shop.models.cart import Cart
from shop.models.order import Order
from shop.models.product import Product, ProductCategory
from shop.models.storage import Storage


class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'active', 'file_name', 'active_file_upload', 'added', 'updated')
    list_display_links = ('id', 'name', 'email', 'active', 'file_name', 'active_file_upload', 'added', 'updated')
    search_fields = ('name', 'email')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated', 'address')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'sku', 'product_category', 'description', '_image')
    list_display_links = ('id', 'brand', 'sku', 'product_category', 'description', '_image')
    search_fields = ('brand', 'sku', 'product_category')


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'russian_name', 'description', 'brands', 'added')
    list_display_links = ('id', 'name', 'russian_name', 'description', 'brands', 'added')
    search_fields = ('name', 'russian_name', 'brands')

    def queryset(self, request):
        return ProductCategory.objects


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Storage, StorageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
