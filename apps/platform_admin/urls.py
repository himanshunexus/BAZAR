from django.urls import path
from . import views

app_name = 'platform_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Shops
    path('shops/', views.shop_list, name='shops'),
    path('shops/<int:pk>/action/', views.shop_action, name='shop_action'),
    # Products
    path('products/', views.product_list, name='products'),
    path('products/<int:pk>/action/', views.product_action, name='product_action'),
    # Users
    path('users/', views.user_list, name='users'),
    path('users/<int:pk>/action/', views.user_action, name='user_action'),
    # Reviews
    path('reviews/', views.review_list, name='reviews'),
    path('reviews/<int:pk>/action/', views.review_action, name='review_action'),
    # Categories
    path('categories/', views.category_list, name='categories'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    # Featured
    path('featured/', views.featured_shops, name='featured'),
    # Analytics
    path('analytics/', views.analytics_page, name='analytics'),
]
