from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.shop_list, name='list'),
    path('create/', views.shop_create, name='create'),
    path('dashboard/', views.seller_dashboard, name='dashboard'),
    path('edit/', views.shop_edit, name='edit'),
    path('pdf-catalog/', views.pdf_catalog, name='pdf_catalog'),
    path('<slug:slug>/', views.shop_detail, name='detail'),
]
