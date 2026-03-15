from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Product, ProductCategory, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'discounted_price', 'stock', 'unit', 'is_active')
        export_order = fields


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'shop', 'price', 'discounted_price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'shop', 'category')
    search_fields = ('name', 'description', 'shop__name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'stock')
    inlines = [ProductImageInline]
