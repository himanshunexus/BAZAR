"""
Management command to seed essential data for BAZAR.
Creates shop categories and product categories so the platform
is usable immediately after a fresh deployment.
"""

from django.core.management.base import BaseCommand

from apps.products.models import ProductCategory
from apps.shops.models import Category


SHOP_CATEGORIES = [
    {'name': 'Grocery & Kirana', 'slug': 'grocery', 'icon': '🛒', 'order': 1},
    {'name': 'Electronics', 'slug': 'electronics', 'icon': '📱', 'order': 2},
    {'name': 'Clothing & Fashion', 'slug': 'clothing', 'icon': '👗', 'order': 3},
    {'name': 'Pharmacy', 'slug': 'pharmacy', 'icon': '💊', 'order': 4},
    {'name': 'Bakery & Sweets', 'slug': 'bakery', 'icon': '🍰', 'order': 5},
    {'name': 'Fruits & Vegetables', 'slug': 'fruits-vegetables', 'icon': '🥬', 'order': 6},
    {'name': 'Hardware & Tools', 'slug': 'hardware', 'icon': '🔧', 'order': 7},
    {'name': 'Stationery & Books', 'slug': 'stationery', 'icon': '📚', 'order': 8},
    {'name': 'Beauty & Salon', 'slug': 'beauty', 'icon': '💇', 'order': 9},
    {'name': 'Restaurant & Food', 'slug': 'restaurant', 'icon': '🍽️', 'order': 10},
    {'name': 'Home & Kitchen', 'slug': 'home-kitchen', 'icon': '🏠', 'order': 11},
    {'name': 'Sports & Fitness', 'slug': 'sports', 'icon': '⚽', 'order': 12},
]

PRODUCT_CATEGORIES = [
    {'name': 'Rice & Grains', 'slug': 'rice-grains'},
    {'name': 'Dal & Pulses', 'slug': 'dal-pulses'},
    {'name': 'Cooking Oil', 'slug': 'cooking-oil'},
    {'name': 'Spices & Masala', 'slug': 'spices-masala'},
    {'name': 'Snacks & Biscuits', 'slug': 'snacks-biscuits'},
    {'name': 'Beverages', 'slug': 'beverages'},
    {'name': 'Dairy & Eggs', 'slug': 'dairy-eggs'},
    {'name': 'Personal Care', 'slug': 'personal-care'},
    {'name': 'Cleaning & Household', 'slug': 'cleaning-household'},
    {'name': 'Mobile Accessories', 'slug': 'mobile-accessories'},
    {'name': 'Clothing - Men', 'slug': 'clothing-men'},
    {'name': 'Clothing - Women', 'slug': 'clothing-women'},
    {'name': 'Medicines', 'slug': 'medicines'},
    {'name': 'Fresh Fruits', 'slug': 'fresh-fruits'},
    {'name': 'Fresh Vegetables', 'slug': 'fresh-vegetables'},
]


class Command(BaseCommand):
    help = 'Seed essential categories for BAZAR marketplace'

    def handle(self, *args, **options):
        shop_created = 0
        for data in SHOP_CATEGORIES:
            _, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if created:
                shop_created += 1

        prod_created = 0
        for data in PRODUCT_CATEGORIES:
            _, created = ProductCategory.objects.get_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if created:
                prod_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {shop_created} shop categories, {prod_created} product categories.'
        ))
