from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'is_seller', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_seller', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('-date_joined',)
    list_editable = ('is_active', 'is_verified', 'is_seller')
    actions = ['verify_users', 'block_users', 'make_seller']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_seller', 'is_verified')}),
        ('Groups', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_seller'),
        }),
    )

    @admin.action(description='Verify selected users')
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description='Block selected users')
    def block_users(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Make selected users sellers')
    def make_seller(self, request, queryset):
        queryset.update(is_seller=True)
