from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Seller product management
    path('manage/', views.product_list_seller, name='seller_list'),
    path('add/', views.product_add, name='add'),
    path('edit/<int:pk>/', views.product_edit, name='edit'),
    path('delete/<int:pk>/', views.product_delete, name='delete'),
    path('bulk-import/', views.bulk_import, name='bulk_import'),
    # Public product detail
    path('<slug:shop_slug>/<slug:slug>/', views.product_detail, name='detail'),
]
