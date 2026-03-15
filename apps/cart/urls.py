from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.cart_add, name='add'),
    path('update/<int:product_id>/', views.cart_update, name='update'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    # Seller order management
    path('orders/', views.seller_orders, name='seller_orders'),
    path('orders/<uuid:order_id>/', views.seller_order_detail, name='seller_order_detail'),
]

# Import payment views safely — don't break all cart URLs if razorpay is missing
try:
    from .payment import create_order, payment_callback
    urlpatterns += [
        path('payment/create/', create_order, name='payment_create'),
        path('payment/callback/', payment_callback, name='payment_callback'),
    ]
except ImportError:
    pass
