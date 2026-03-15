from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('cities/', views.city_select, name='city_select'),
    path('category/<slug:slug>/', views.category_page, name='category'),
    path('search/', views.search, name='search'),
]
