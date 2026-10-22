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
    {
        'email': 'demo-clothing@bazar.local', 'name': 'Demo Everyday Clothing',
        'slug': 'demo-everyday-clothing', 'category': 'clothing',
        'description': 'A sample neighborhood clothing shop. Demo listings only.',
        'address': 'Demo Clothing Market', 'city': 'Bengaluru', 'pincode': '560004',
        'contact_phone': '910000000004', 'products': [],
    },
    {
        'email': 'demo-pharmacy@bazar.local', 'name': 'Demo Neighborhood Pharmacy',
        'slug': 'demo-neighborhood-pharmacy', 'category': 'pharmacy',
        'description': 'A sample neighborhood pharmacy. Demo listings only.',
        'address': 'Demo Health Street', 'city': 'Bengaluru', 'pincode': '560005',
        'contact_phone': '910000000005', 'products': [],
    },
]

# Ten catalog entries are available for every product category. Existing demo
# listings count toward the total, so the seed fills only the remaining slots.
# Photos are reused by category in Cloudinary to keep startup uploads small.
EXPANDED_CATALOG = {
    'rice-grains': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 72,
        'image': 'photo-1586201375761-83865001e31c',
        'products': ['Sona Masoori Rice', 'Basmati Rice', 'Kolam Rice', 'Idli Rice', 'Brown Rice', 'Raw Ponni Rice', 'Steamed Rice', 'Poha (Flattened Rice)', 'Whole Wheat Atta', 'Ragi Flour'],
    },
    'dal-pulses': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 110,
        'image': 'photo-1515543904379-3d757afe72e4',
        'products': ['Toor Dal', 'Moong Dal', 'Masoor Dal', 'Chana Dal', 'Urad Dal', 'Kabuli Chana', 'Black Chana', 'Whole Green Moong', 'Rajma', 'White Peas'],
    },
    'cooking-oil': {
        'shop': 'demo-fresh-market', 'unit': 'litre', 'price': 145,
        'image': 'photo-1474979266404-7eaacbcd87c5',
        'products': ['Sunflower Oil', 'Groundnut Oil', 'Mustard Oil', 'Rice Bran Oil', 'Coconut Oil', 'Sesame Oil', 'Soybean Oil', 'Olive Oil', 'Ghee', 'Cold-Pressed Groundnut Oil'],
    },
    'spices-masala': {
        'shop': 'demo-fresh-market', 'unit': '100 g', 'price': 45,
        'image': 'photo-1532336414038-cf19250c5757',
        'products': ['Turmeric Powder', 'Red Chilli Powder', 'Coriander Powder', 'Cumin Seeds', 'Garam Masala', 'Black Pepper', 'Mustard Seeds', 'Cardamom', 'Cinnamon Sticks', 'Kitchen King Masala'],
    },
    'snacks-biscuits': {
        'shop': 'demo-corner-bakery', 'unit': 'pack', 'price': 35,
        'image': 'photo-1738898326912-83ec04de4ccf',
        'products': ['Butter Cookies', 'Salted Potato Chips', 'Masala Peanuts', 'Cream Biscuits', 'Rusk Toast', 'Chocolate Cookies', 'Banana Chips', 'Crackers', 'Baked Mathri', 'Mixed Namkeen'],
    },
    'beverages': {
        'shop': 'demo-corner-bakery', 'unit': 'piece', 'price': 30,
        'image': 'photo-1602101888216-252a1aeead4a',
        'products': ['Filter Coffee', 'Assam Tea', 'Green Tea', 'Mango Juice', 'Orange Juice', 'Lemon Soda', 'Coconut Water', 'Hot Chocolate', 'Cold Coffee', 'Masala Chai'],
    },
    'dairy-eggs': {
        'shop': 'demo-fresh-market', 'unit': 'pack', 'price': 65,
        'image': 'photo-1563636619-e9143da7973b',
        'products': ['Toned Milk', 'Full Cream Milk', 'Curd', 'Paneer', 'Butter', 'Cheddar Cheese', 'Fresh Cream', 'Buttermilk', 'Farm Eggs (6)', 'Farm Eggs (12)'],
    },
    'personal-care': {
        'shop': 'demo-fresh-market', 'unit': 'piece', 'price': 85,
        'image': 'photo-1608248543803-ba4f8c70ae0b',
        'products': ['Aloe Vera Face Wash', 'Herbal Shampoo', 'Coconut Hair Oil', 'Bathing Soap', 'Toothpaste', 'Toothbrush', 'Body Lotion', 'Hand Wash', 'Sunscreen SPF 30', 'Deodorant'],
    },
    'cleaning-household': {
        'shop': 'demo-fresh-market', 'unit': 'piece', 'price': 75,
        'image': 'photo-1585421514738-01798e348b17',
        'products': ['Laundry Detergent', 'Dishwashing Liquid', 'Floor Cleaner', 'Toilet Cleaner', 'Glass Cleaner', 'Scrub Sponge Set', 'Garbage Bags', 'Microfiber Cloth', 'Room Freshener', 'Disinfectant Spray'],
    },
    'mobile-accessories': {
        'shop': 'demo-mobile-and-more', 'unit': 'piece', 'price': 299,
        'image': 'photo-1588182464121-05a6397e3a5b',
        'products': ['USB-C Charging Cable', '20W Fast Charger', 'Wireless Earbuds', 'Phone Case', 'Tempered Glass Screen Guard', 'Power Bank 10000mAh', 'Bluetooth Speaker', 'Car Phone Mount', 'Wired Earphones', 'USB-C OTG Adapter'],
    },
    'clothing-men': {
        'shop': 'demo-everyday-clothing', 'unit': 'piece', 'price': 499,
        'image': 'photo-1523381210434-271e8be1f52b',
        'products': ['Classic Cotton T-Shirt', 'Casual Oxford Shirt', 'Everyday Polo Shirt', 'Slim Fit Jeans', 'Cotton Chinos', 'Lightweight Hoodie', 'Checked Casual Shirt', 'Cotton Kurta', 'Track Pants', 'Denim Jacket'],
    },
    'clothing-women': {
        'shop': 'demo-everyday-clothing', 'unit': 'piece', 'price': 599,
        'image': 'photo-1483985988355-763728e1935b',
        'products': ['Cotton Kurti', 'Everyday Top', 'Floral Summer Dress', 'Straight Fit Jeans', 'Cotton Leggings', 'Printed Dupatta', 'Linen Shirt', 'Casual Palazzo Pants', 'Knit Cardigan', 'Traditional Saree'],
    },
    'medicines': {
        'shop': 'demo-neighborhood-pharmacy', 'unit': 'pack', 'price': 50,
        'image': 'photo-1584308666744-24d5c474f2ae',
        'products': ['Digital Thermometer', 'Adhesive Bandages', 'Antiseptic Liquid', 'Cotton Roll', 'Oral Rehydration Salts', 'Vitamin C Tablets', 'Hand Sanitizer', 'Hot Water Bag', 'First Aid Kit', 'Disposable Face Masks'],
    },
    'fresh-fruits': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 90,
        'image': 'photo-1610832958506-aa56368176cf',
        'products': ['Alphonso Mangoes', 'Nagpur Oranges', 'Kashmir Apples', 'Robusta Bananas', 'Green Grapes', 'Pomegranate', 'Papaya', 'Sweet Lime', 'Pineapple', 'Watermelon'],
    },
    'fresh-vegetables': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 55,
        'image': 'photo-1714224247661-ee250f55a842',
        'products': ['Tomatoes', 'Potatoes', 'Red Onions', 'Carrots', 'Spinach', 'Cauliflower', 'Green Capsicum', 'Cucumber', 'Green Beans', 'Fresh Coriander'],
    },
}

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

        shops_by_slug = {}
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
            shops_by_slug[shop.slug] = shop
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

        # Fill each product category to exactly ten listings across the demo
        # shops. The original hand-picked demo listings count toward the total.
        for category_slug, catalog in EXPANDED_CATALOG.items():
            category = ProductCategory.objects.get(slug=category_slug)
            shop = shops_by_slug[catalog['shop']]
            count = Product.objects.filter(
                category=category,
                shop__slug__in=shops_by_slug.keys(),
                is_active=True,
            ).count()
            needed = max(0, 10 - count)
            image_url = (
                f"https://images.unsplash.com/{catalog['image']}"
                '?auto=format&fit=crop&fm=jpg&q=80&w=1200'
            )
            public_id = f'bazar-demo/categories/{category_slug}'
            cloudinary_public_id = f'media/{public_id}'
            image_available = False
            if cloudinary_enabled:
                try:
                    try:
                        api.resource(cloudinary_public_id, resource_type='image')
                    except Exception:
                        uploader.upload(
                            image_url,
                            public_id=cloudinary_public_id,
                            resource_type='image',
                        )
                    image_available = True
                except Exception as exc:
                    self.stderr.write(self.style.WARNING(
                        f'Could not sync category image for {category_slug}: {exc}'
                    ))
            for index, name in enumerate(catalog['products'], start=1):
                product = Product.objects.filter(
                    shop=shop, slug=slugify(name), category=category,
                ).first()
                if product is None:
                    if needed == 0:
                        break
                    product, _ = Product.objects.update_or_create(
                        shop=shop, slug=slugify(name),
                        defaults={
                            'name': name,
                            'description': f'{name}, available from a local demo shop. Demo listing; confirm availability with the shop.',
                            'category': category,
                            'price': catalog['price'] + (index - 1) * 7,
                            'stock': 10,
                            'unit': catalog['unit'],
                            'is_active': True,
                        },
                    )
                    needed -= 1
                elif not product.is_active and needed > 0:
                    product.is_active = True
                    product.save(update_fields=['is_active', 'updated_at'])
                    needed -= 1
                if not image_available:
                    continue
                try:
                    ProductImage.objects.update_or_create(
                        product=product, order=0,
                        defaults={
                            'image': public_id,
                            'alt_text': f'{name} — category photo',
                        },
                    )
                except Exception as exc:
                    self.stderr.write(self.style.WARNING(
                        f'Could not sync demo image for {name}: {exc}'
                    ))
