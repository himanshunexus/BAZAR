"""Management command to seed essential data for BAZAR.
Creates shop categories and product categories so the platform
is usable immediately after a fresh deployment.
"""

import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from apps.products.models import Product, ProductCategory, ProductImage
from apps.shops.models import Category, Shop


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

# Unsplash images are uploaded once to Cloudinary. Attribution is kept with
# each image record so it remains visible in the admin/catalog data.
DEMO_SHOPS = [
    {
        'email': 'demo-grocery@bazar.local', 'name': 'Demo Fresh Market',
        'slug': 'demo-fresh-market', 'category': 'grocery',
        'description': 'A sample neighborhood grocery shop. Demo listings only.',
        'address': 'Demo Market Road', 'city': 'Bengaluru', 'pincode': '560001',
        'contact_phone': '910000000001', 'products': [
            ('Seasonal Fresh Produce (Demo)', 'fresh-vegetables', 'Fresh seasonal produce display. Demo listing; confirm availability with the shop.', 85, 'kg', 'https://images.unsplash.com/photo-1714224247661-ee250f55a842?auto=format&fit=crop&fm=jpg&q=80&w=1200', 'Photo by mintolime on Unsplash'),
            ('Market Vegetables (Demo)', 'fresh-vegetables', 'Colorful market vegetables. Demo listing; confirm availability with the shop.', 60, 'kg', 'https://images.unsplash.com/photo-1715944486739-d32f7852a66f?auto=format&fit=crop&fm=jpg&q=80&w=1200', 'Photo by Ana Bacon on Unsplash'),
            ('Fresh Fruit Selection (Demo)', 'fresh-fruits', 'A sample fresh fruit selection. Demo listing; confirm availability with the shop.', 120, 'kg', 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&fm=jpg&q=80&w=1200', 'Unsplash photo'),
        ],
    },
    {
        'email': 'demo-bakery@bazar.local', 'name': 'Demo Corner Bakery',
        'slug': 'demo-corner-bakery', 'category': 'bakery',
        'description': 'A sample local bakery. Demo listings only.',
        'address': 'Demo Bakery Lane', 'city': 'Bengaluru', 'pincode': '560002',
        'contact_phone': '910000000002', 'products': [
            ('Fresh Bakery Assortment (Demo)', 'snacks-biscuits', 'Sample bakery assortment. Demo listing; confirm availability with the shop.', 180, 'box', 'https://images.unsplash.com/photo-1738898326912-83ec04de4ccf?auto=format&fit=crop&fm=jpg&q=80&w=1200', 'Photo by wei on Unsplash'),
            ('Coffee Beans (Demo)', 'beverages', 'A sample coffee product. Demo listing; confirm availability with the shop.', 350, '250 g', 'https://images.unsplash.com/photo-1602101888216-252a1aeead4a?auto=format&fit=crop&fm=jpg&q=80&w=1200', 'Photo by Oscar Helgstrand on Unsplash'),
        ],
    },
    {
        'email': 'demo-electronics@bazar.local', 'name': 'Demo Mobile & More',
        'slug': 'demo-mobile-and-more', 'category': 'electronics',
        'description': 'A sample neighborhood electronics shop. Demo listings only.',
        'address': 'Demo Electronics Street', 'city': 'Bengaluru', 'pincode': '560003',
        'contact_phone': '910000000003', 'products': [
            ('Smartphone (Demo)', 'mobile-accessories', 'Sample smartphone listing. Demo listing; confirm availability with the shop.', 14999, 'piece', 'https://images.unsplash.com/photo-1588182464121-05a6397e3a5b?auto=format&fit=crop&fm=jpg&q=80&w=1200', 'Photo by Amaan Ali on Unsplash'),
        ],
    },
]

DEMO_ROLES = [
    ('DEMO_ADMIN_EMAIL', 'DEMO_ADMIN_PASSWORD', 'admin@bazar.local', 'BAZAR Demo Admin', 'admin'),
    ('DEMO_SELLER_EMAIL', 'DEMO_SELLER_PASSWORD', 'demo-grocery@bazar.local', 'Demo Seller', 'seller'),
    ('DEMO_CUSTOMER_EMAIL', 'DEMO_CUSTOMER_PASSWORD', 'customer@bazar.local', 'Demo Customer', 'customer'),
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

        self._seed_demo_users()
        self._seed_demo_catalog()

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {shop_created} shop categories, {prod_created} product categories.'
        ))

    def _seed_demo_users(self):
        User = get_user_model()
        for email_key, password_key, default_email, name, role in DEMO_ROLES:
            # Shop owners must use the fixed demo email referenced by DEMO_SHOPS.
            # Allowing a separate override here can leave the catalog without an owner.
            email = default_email if role == 'seller' else os.environ.get(email_key, default_email)
            password = os.environ.get(password_key, '')
            defaults = {
                'full_name': name,
                'is_seller': role == 'seller',
                'is_verified': True,
                'is_staff': role == 'admin',
                'is_superuser': role == 'admin',
            }
            user, created = User.objects.get_or_create(email=email, defaults=defaults)
            # Demo accounts are password-enabled only when Render env vars are set.
            if password:
                user.set_password(password)
            elif created:
                user.set_unusable_password()
            user.full_name = name
            user.is_seller = role == 'seller'
            user.is_verified = True
            user.is_staff = role == 'admin'
            user.is_superuser = role == 'admin'
            user.save()

    def _seed_demo_catalog(self):
        try:
            import cloudinary
            from cloudinary import api, uploader
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'),
                api_key=settings.CLOUDINARY_STORAGE.get('API_KEY'),
                api_secret=settings.CLOUDINARY_STORAGE.get('API_SECRET'),
                secure=True,
            )
            cloudinary_enabled = all((
                settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'),
                settings.CLOUDINARY_STORAGE.get('API_KEY'),
                settings.CLOUDINARY_STORAGE.get('API_SECRET'),
            ))
        except Exception:
            cloudinary_enabled = False
            uploader = None

        for shop_data in DEMO_SHOPS:
            seller, _ = get_user_model().objects.get_or_create(
                email=shop_data['email'],
                defaults={
                    'full_name': 'Demo Seller',
                    'is_seller': True,
                    'is_verified': True,
                },
            )
            seller.is_seller = True
            seller.is_verified = True
            seller.save(update_fields=['is_seller', 'is_verified'])
            category = Category.objects.get(slug=shop_data['category'])
            shop, _ = Shop.objects.update_or_create(
                owner=seller,
                defaults={
                    'name': shop_data['name'], 'slug': shop_data['slug'],
                    'category': category, 'description': shop_data['description'],
                    'address': shop_data['address'], 'city': shop_data['city'],
                    'pincode': shop_data['pincode'], 'state': 'Karnataka',
                    'contact_phone': shop_data['contact_phone'],
                    'whatsapp_phone': shop_data['contact_phone'],
                    'is_verified': True, 'is_active': True,
                },
            )
            for name, category_slug, description, price, unit, image_url, attribution in shop_data['products']:
                product_category = ProductCategory.objects.get(slug=category_slug)
                product, _ = Product.objects.update_or_create(
                    shop=shop, slug=slugify(name),
                    defaults={
                        'name': name, 'description': description,
                        'category': product_category, 'price': price,
                        'stock': 10, 'unit': unit, 'is_active': True,
                    },
                )
                if not cloudinary_enabled:
                    continue
                public_id = f"bazar-demo/products/{shop.slug}-{product.slug}"
                cloudinary_public_id = f"media/{public_id}"
                try:
                    try:
                        api.resource(cloudinary_public_id, resource_type='image')
                    except Exception:
                        uploader.upload(image_url, public_id=cloudinary_public_id, resource_type='image')
                    ProductImage.objects.update_or_create(
                        product=product, order=0,
                        defaults={'image': public_id, 'alt_text': f'{name} — {attribution}'},
                    )
                except Exception as exc:
                    self.stderr.write(self.style.WARNING(
                        f'Could not sync demo image for {name}: {exc}'
                    ))
