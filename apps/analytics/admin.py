from django.contrib import admin
from .models import ShopAnalytics


@admin.register(ShopAnalytics)
class ShopAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('shop', 'date', 'views', 'clicks', 'product_views', 'whatsapp_clicks')
    list_filter = ('date', 'shop')
    readonly_fields = ('shop', 'date', 'views', 'clicks', 'product_views', 'whatsapp_clicks')
