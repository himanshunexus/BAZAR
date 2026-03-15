from django.contrib import admin
from .models import Category, Shop


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)
    search_fields = ('name',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'pincode', 'category', 'is_verified', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_verified', 'is_featured', 'is_active', 'city', 'category')
    search_fields = ('name', 'city', 'pincode', 'owner__email')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_verified', 'is_featured', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_shops', 'verify_shops', 'suspend_shops', 'feature_shops']

    @admin.action(description='Approve & verify selected shops')
    def approve_shops(self, request, queryset):
        queryset.update(is_verified=True, is_active=True)

    @admin.action(description='Verify selected shops')
    def verify_shops(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description='Suspend selected shops')
    def suspend_shops(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Feature selected shops')
    def feature_shops(self, request, queryset):
        queryset.update(is_featured=True)
