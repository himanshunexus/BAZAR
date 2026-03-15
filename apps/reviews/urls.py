from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('shop/<slug:shop_slug>/', views.add_shop_review, name='add_shop_review'),
]
