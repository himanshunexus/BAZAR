"""Seed categories, demo shops, and a photo-complete starter catalog."""

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

# Each demo shop has its own storefront cover and logo photo. Product image
# sources are maintained separately in CATALOG_IMAGE_URLS, one URL per item.
DEMO_SHOPS = [
    {
        'email': 'demo-grocery@bazar.local', 'name': 'Demo Fresh Market',
        'slug': 'demo-fresh-market', 'category': 'grocery',
        'banner_image': 'photo-1542838132-92c53300491e',
        'logo_image': 'photo-1540420773420-3366772f4999',
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
        'banner_image': 'photo-1509440159596-0249088772ff',
        'logo_image': 'photo-1555507036-ab1f4038808a',
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
        'banner_image': 'photo-1511707171634-5f897ff02aa9',
        'logo_image': 'photo-1512499617640-c74ae3a79d37',
        'description': 'A sample neighborhood electronics shop. Demo listings only.',
        'address': 'Demo Electronics Street', 'city': 'Bengaluru', 'pincode': '560003',
        'contact_phone': '910000000003', 'products': [
            ('Smartphone (Demo)', 'mobile-accessories', 'Sample smartphone listing. Demo listing; confirm availability with the shop.', 14999, 'piece', 'https://images.unsplash.com/photo-1588182464121-05a6397e3a5b?auto=format&fit=crop&fm=jpg&q=80&w=1200', 'Photo by Amaan Ali on Unsplash'),
        ],
    },
    {
        'email': 'demo-clothing@bazar.local', 'name': 'Demo Everyday Clothing',
        'slug': 'demo-everyday-clothing', 'category': 'clothing',
        'banner_image': 'photo-1445205170230-053b83016050',
        'logo_image': 'photo-1483985988355-763728e1935b',
        'description': 'A sample neighborhood clothing shop. Demo listings only.',
        'address': 'Demo Clothing Market', 'city': 'Bengaluru', 'pincode': '560004',
        'contact_phone': '910000000004', 'products': [],
    },
    {
        'email': 'demo-pharmacy@bazar.local', 'name': 'Demo Neighborhood Pharmacy',
        'slug': 'demo-neighborhood-pharmacy', 'category': 'pharmacy',
        'banner_image': 'photo-1576091160399-112ba8d25d1d',
        'logo_image': 'photo-1559757175-0eb30cd8c063',
        'description': 'A sample neighborhood pharmacy. Demo listings only.',
        'address': 'Demo Health Street', 'city': 'Bengaluru', 'pincode': '560005',
        'contact_phone': '910000000005', 'products': [],
    },
]

# Ten catalog entries are available for every product category. Existing demo
# listings count toward the total, and each seeded product receives its own photo.
EXPANDED_CATALOG = {
    'rice-grains': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 72,
        'products': ['Sona Masoori Rice', 'Basmati Rice', 'Kolam Rice', 'Idli Rice', 'Brown Rice', 'Raw Ponni Rice', 'Steamed Rice', 'Poha (Flattened Rice)', 'Whole Wheat Atta', 'Ragi Flour'],
    },
    'dal-pulses': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 110,
        'products': ['Toor Dal', 'Moong Dal', 'Masoor Dal', 'Chana Dal', 'Urad Dal', 'Kabuli Chana', 'Black Chana', 'Whole Green Moong', 'Rajma', 'White Peas'],
    },
    'cooking-oil': {
        'shop': 'demo-fresh-market', 'unit': 'litre', 'price': 145,
        'products': ['Sunflower Oil', 'Groundnut Oil', 'Mustard Oil', 'Rice Bran Oil', 'Coconut Oil', 'Sesame Oil', 'Soybean Oil', 'Olive Oil', 'Ghee', 'Cold-Pressed Groundnut Oil'],
    },
    'spices-masala': {
        'shop': 'demo-fresh-market', 'unit': '100 g', 'price': 45,
        'products': ['Turmeric Powder', 'Red Chilli Powder', 'Coriander Powder', 'Cumin Seeds', 'Garam Masala', 'Black Pepper', 'Mustard Seeds', 'Cardamom', 'Cinnamon Sticks', 'Kitchen King Masala'],
    },
    'snacks-biscuits': {
        'shop': 'demo-corner-bakery', 'unit': 'pack', 'price': 35,
        'products': ['Butter Cookies', 'Salted Potato Chips', 'Masala Peanuts', 'Cream Biscuits', 'Rusk Toast', 'Chocolate Cookies', 'Banana Chips', 'Crackers', 'Baked Mathri', 'Mixed Namkeen'],
    },
    'beverages': {
        'shop': 'demo-corner-bakery', 'unit': 'piece', 'price': 30,
        'products': ['Filter Coffee', 'Assam Tea', 'Green Tea', 'Mango Juice', 'Orange Juice', 'Lemon Soda', 'Coconut Water', 'Hot Chocolate', 'Cold Coffee', 'Masala Chai'],
    },
    'dairy-eggs': {
        'shop': 'demo-fresh-market', 'unit': 'pack', 'price': 65,
        'products': ['Toned Milk', 'Full Cream Milk', 'Curd', 'Paneer', 'Butter', 'Cheddar Cheese', 'Fresh Cream', 'Buttermilk', 'Farm Eggs (6)', 'Farm Eggs (12)'],
    },
    'personal-care': {
        'shop': 'demo-fresh-market', 'unit': 'piece', 'price': 85,
        'products': ['Aloe Vera Face Wash', 'Herbal Shampoo', 'Coconut Hair Oil', 'Bathing Soap', 'Toothpaste', 'Toothbrush', 'Body Lotion', 'Hand Wash', 'Sunscreen SPF 30', 'Deodorant'],
    },
    'cleaning-household': {
        'shop': 'demo-fresh-market', 'unit': 'piece', 'price': 75,
        'products': ['Laundry Detergent', 'Dishwashing Liquid', 'Floor Cleaner', 'Toilet Cleaner', 'Glass Cleaner', 'Scrub Sponge Set', 'Garbage Bags', 'Microfiber Cloth', 'Room Freshener', 'Disinfectant Spray'],
    },
    'mobile-accessories': {
        'shop': 'demo-mobile-and-more', 'unit': 'piece', 'price': 299,
        'products': ['USB-C Charging Cable', '20W Fast Charger', 'Wireless Earbuds', 'Phone Case', 'Tempered Glass Screen Guard', 'Power Bank 10000mAh', 'Bluetooth Speaker', 'Car Phone Mount', 'Wired Earphones', 'USB-C OTG Adapter'],
    },
    'clothing-men': {
        'shop': 'demo-everyday-clothing', 'unit': 'piece', 'price': 499,
        'products': ['Classic Cotton T-Shirt', 'Casual Oxford Shirt', 'Everyday Polo Shirt', 'Slim Fit Jeans', 'Cotton Chinos', 'Lightweight Hoodie', 'Checked Casual Shirt', 'Cotton Kurta', 'Track Pants', 'Denim Jacket'],
    },
    'clothing-women': {
        'shop': 'demo-everyday-clothing', 'unit': 'piece', 'price': 599,
        'products': ['Cotton Kurti', 'Everyday Top', 'Floral Summer Dress', 'Straight Fit Jeans', 'Cotton Leggings', 'Printed Dupatta', 'Linen Shirt', 'Casual Palazzo Pants', 'Knit Cardigan', 'Traditional Saree'],
    },
    'medicines': {
        'shop': 'demo-neighborhood-pharmacy', 'unit': 'pack', 'price': 50,
        'products': ['Digital Thermometer', 'Adhesive Bandages', 'Antiseptic Liquid', 'Cotton Roll', 'Oral Rehydration Salts', 'Vitamin C Tablets', 'Hand Sanitizer', 'Hot Water Bag', 'First Aid Kit', 'Disposable Face Masks'],
    },
    'fresh-fruits': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 90,
        'products': ['Alphonso Mangoes', 'Nagpur Oranges', 'Kashmir Apples', 'Robusta Bananas', 'Green Grapes', 'Pomegranate', 'Papaya', 'Sweet Lime', 'Pineapple', 'Watermelon'],
    },
    'fresh-vegetables': {
        'shop': 'demo-fresh-market', 'unit': 'kg', 'price': 55,
        'products': ['Tomatoes', 'Potatoes', 'Red Onions', 'Carrots', 'Spinach', 'Cauliflower', 'Green Capsicum', 'Cucumber', 'Green Beans', 'Fresh Coriander'],
    },
}

CATALOG_IMAGE_URLS = {
    "rice-grains": [
        "https://veehafoods.com/cdn/shop/files/8906055441596_06_9714be72-40f3-4690-bbaa-3125a497d64f.png?crop=center&height=1080&v=1728638349&width=1080",
        "https://cdn.d4tcdn.com/uploaded_files/helpimgs/difference-between-1509-and-1121-basmati-rice-price-which-one-is-better-5389a8d.jpg",
        "https://www.tradologie.com/docs/images/organic-soul-basmati-rice.webp",
        "https://futureconsumer.in/assets/img/brands/mother-earth-rice.jpg",
        "https://ph-live-01.slatic.net/p/a9e8b6072a510ddb1f8f5d3dc504ffc0.jpg",
        "https://pansaridirect.com/master/Product/4521744356335_M_0.jpg",
        "https://images.unsplash.com/photo-1651793371427-ad065df0d208?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://izoleapv4-prod-assets.s3.amazonaws.com/izoleap_m_16/pims/category/Rice%20and%20rice%20products-image-1745988494852.webp",
        "https://images.happycow.net/venues/1024/22/04/hcmp220499_1024719.jpeg",
        "https://i5.walmartimages.com/asr/1b89b2a2-fd1b-47ec-8b6f-f2a09a3ab1d0.4b1c9a0ebc1880be5958f2ac8deb5009.jpeg",
    ],
    "dal-pulses": [
        "https://i.ebayimg.com/images/g/1OkAAOSwnL9nkiJR/s-l1200.jpg",
        "https://www.par.com.pk/assets/images/pulses_pg.webp",
        "https://images.unsplash.com/photo-1612257416648-ee7a6c533b4f?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://images.bhaskarassets.com/web2images/521/2024/12/28/f9b7d6c2-c0e2-4b21-8b2c-19164feab1e2_1735389432284.jpg",
        "https://dogruhabercomtr.teimg.com/crop/1280x720/dogruhaber-com-tr/images/2024/1/12/641e30eeb00c43079c0f447f4de39f48-gecen-yil-630-bin-ton-nohut-44-bin-ton-yesil-mercimek-uretildi-16a3e492.jpg",
        "https://www.blazze.world/Photos/Final%20PULSES%20IMAGE.webp",
        "https://img500.exportersindia.com/product_images/bc-500/dir_112/3349652/pulses-1698426.jpg",
        "https://down-my.img.susercontent.com/file/sg-11134201-7rdxv-mdk0tyxnuy4q44",
        "https://www.dial4trade.com/uploaded_files/product_images/thumbs/pulses-u-1267952227312510806.png",
        "https://dam.buhlergroup.com/image/8186d78b7a31493ea18fbd46603d8c0e/-FJPG-C2880x2160%2C267%2C0-S600x450-S1024x768",
    ],
    "cooking-oil": [
        "https://organictattva.com/cdn/shop/files/1_7_1599f176-65ff-4283-9079-9e69a98738b7.png?v=1777794126&width=1200",
        "https://static.wixstatic.com/media/97db43_78d9c505ac6c4424982fdfb2b79e42d1~mv2.jpg/v1/fit/w_613%2Ch_616%2Cq_90%2Cenc_avif%2Cquality_auto/97db43_78d9c505ac6c4424982fdfb2b79e42d1~mv2.jpg",
        "https://shuddhayuoils.com/cdn/shop/files/sunflower-groundnut-mustard-combo-1ltr.jpg?v=1754140530&width=533",
        "https://cdn.shopify.com/s/files/1/0607/3660/2286/files/Combo_Oil_Product_Image.jpg?v=1765358296",
        "https://i5.walmartimages.com/seo/Rani-Premium-Oils-Combo-Set-3-Peanut-Oil-Mustard-Sesame-Oil-16-9-Ounce-500ml-Cold-Pressed-100-Natural-NON-GMO-Vegan-Gluten-Free_27f9547b-252b-4902-b604-59b106a8c921.5ea88c71f4351a1ed9901c3981c6828a.jpeg?odnBg=FFFFFF&odnHeight=580&odnWidth=580",
        "https://images.navafresh.io/products/HAAZINB07H6B9FTW/1_61zm3qwQfTL_desktop.jpg",
        "https://sonifarms.in/cdn/shop/files/SF-MUSTARD_SUNFLOWER_GROUNDNUT-OIL-F-JPG-20250616-REV.jpg?v=1750057168",
        "https://images.unsplash.com/photo-1757801333112-7b89af15c7fe?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://img2.exportersindia.com/product_images/bc-full/2022/12/248524/groundnut-oil-1672305894-6694706.jpeg",
        "https://images.unsplash.com/photo-1757801333112-7b89af15c7fe?auto=format&fit=crop&fm=jpg&q=80&w=1200",
    ],
    "spices-masala": [
        "https://makeshop-multi-images.akamaized.net/aarti/itemimages/000000002804_cIeiKiL.jpg",
        "https://exportinc.co.in/assets/img/about.jpg",
        "https://images.unsplash.com/photo-1742748912566-b2f1851e6021?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://desiaroma.in/uploads/products/20260626064512-85d38e44c4f477be.webp",
        "https://images.squarespace-cdn.com/content/v1/60e47800230f946dd901f16d/1629691250406-6WFWKMCM5YB5QB0BH1YN/WhatsApp%2BImage%2B2021-02-02%2Bat%2B12.16.47%2BPM%2B%25281%2529.jpg?format=1500w",
        "https://images.meesho.com/images/products/593921258/aklom_512.webp?width=512",
        "https://www.chaisangroups.com/images/spice-powders-vibrant.png",
        "https://images.unsplash.com/photo-1532336414038-cf19250c5757?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://i0.wp.com/spicechronicles.com/wp-content/uploads/2015/03/Masala_650.jpg?ssl=1",
        "https://amitfoods.com/images/about-img.jpg",
    ],
    "snacks-biscuits": [
        "https://img2.exportersindia.com/product_images/bc-full/2020/12/7373035/bakery-biscuits-1607085234-5648460.jpeg",
        "https://thechanceonlinestore.com/media/categories/Top-Biscuit-Brands-in-700x470.jpg",
        "https://image.cdn.shpy.in/28193/cat/1655723823696_42746_cat.png?format=webp",
        "https://www.groceriescarenepal.com/images/category/1780495592_biscuits.webp",
        "https://cdn.dnaindia.com/sites/default/files/styles/full/public/2017/03/08/554651-biscuits-030817.jpg",
        "https://images.unsplash.com/photo-1704137410635-35882ba43c71?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://packagingsouthasia.com/wp-content/uploads/2020/08/image1.jpg",
        "https://m.media-amazon.com/images/I/91diH9gym8L.jpg",
        "https://cdn.apartmenttherapy.info/image/upload/f_auto%2Cq_auto%3Aeco%2Cw_730/k/Edit/2024-03-grocery-diary-anshuli/d-mart-haul",
        "https://cloudfront-eu-central-1.images.arcpublishing.com/williamreed/7YYSSYEIAFJFZB4ZOQDXUUIIXE.jpg",
    ],
    "beverages": [
        "https://www.eatsprout.com/cdn/shop/collections/1x1_Drinks_5000x.jpg?v=1589468854",
        "https://image.news.livedoor.com/newsimage/stf/2/7/27ddb_1589_6d9a365e_d6483990-sq.jpg",
        "https://info.bytetechnology.co/hubfs/4162_3980_4167_2350_4460_3127_2360%20%281%29.jpg",
        "https://images.squarespace-cdn.com/content/v1/5ef4d9cf0d6ad7677610fdc9/1596055014285-7MHGGCMPE1ZX655ABATF/WhatsApp%2BImage%2B2020-07-16%2Bat%2B10.11.04.jpeg",
        "https://ww2.kqed.org/app/uploads/sites/24/2015/07/group.jpg",
        "https://www.coca-cola.com/content/dam/onexp/zz/en/sustainability/in-our-products/coca-cola-reduced-sugar-products-703x450.png",
        "https://d1d7kfcb5oumx0.cloudfront.net/articles/images/6752e7ad42c16a29061adae8/slide_file.jpg",
        "https://photos1.blogger.com/blogger/3252/1972/1600/106_0672.0.jpg",
        "https://image.hkhl.hk/f/1024p0/0x0/100/none/5ec48823f5c55bebf824b5d985558f2c/2022-04/%E5%8F%AF%E5%8F%A3%E5%8F%AF%E6%A8%823.jpg",
        "https://m.media-amazon.com/images/I/615aKq4AILL._AC_SL1080_.jpg",
    ],
    "dairy-eggs": [
        "https://cf-img-a-in.tosshub.com/sites/visualstory/wp/2024/11/12-7.jpg?size=%2A%3A675",
        "https://c.ndtvimg.com/2020-08/h02cbn6_milk-and-dairy-products-_625x300_18_August_20.jpg?im=FaceCrop%2Calgorithm%3Ddnn%2Cwidth%3D1200%2Cheight%3D675",
        "https://static.wixstatic.com/media/e4e183_ba043d3eae1c46ddaa11adc3c5e52dd8~mv2.png/v1/fill/w_1000%2Ch_774%2Cal_c%2Cq_90%2Cusm_0.66_1.00_0.01/e4e183_ba043d3eae1c46ddaa11adc3c5e52dd8~mv2.png",
        "https://yourviews.mindstick.com/Stories/b88943ca-43f5-49e5-86bf-ecab99f4e8ac/images/b3fdff5a-5f39-46f8-b726-b49bbb0bcd81.jpeg",
        "https://newbusinessage.prixacdn.net/img/news/20230109014440_1673219740.Clipboard11.jpg",
        "https://cdn.knd.ro/media/521/2864/1732/20382412/1/lactate.jpg?height=467&width=700",
        "https://c.ndtvimg.com/2020-05/3mtomfvg_milk_625x300_09_May_20.jpg",
        "https://cf-img-a-in.tosshub.com/sites/visualstory/wp/2024/11/image-2080.png?size=%2A%3A900",
        "https://www.sidomunculstore.com/media/wysiwyg/Jan_2025/1._Susu_dan_Produk_Olahannya.jpg",
        "https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&fm=jpg&q=80&w=1200",
    ],
    "personal-care": [
        "https://bazaarbandhu.com/assets/cat-personal-BFmqqD6v.png",
        "https://di2ponv0v5otw.cloudfront.net/posts/2023/03/23/641c98f2b635f8283b1b6e31/m_641c98fa8bb2e2560e3adde6.jpg",
        "https://image.invaluable.com/housePhotos/theodorebruceauctions/93/763193/H3561-L359492968_original.JPG",
        "https://ds393qgzrxwzn.cloudfront.net/resize/c500x500/cat1/img/images/0/F2iBiNRyVB.jpg",
        "https://static-01.daraz.pk/p/56100dd762681e760f462ed2b4545ed5.jpg",
        "https://i0.wp.com/adventuresofherman.com/content/uploads/2017/10/img_9475.jpeg?fit=3024%2C3024&ssl=1",
        "https://thegivingstore.org.nz/cdn/shop/products/custom_resized_8664376c-f6d6-4a72-9ddc-1a425d44d26d_2048x2048.jpg?v=1600745195",
        "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://imgix.bustle.com/rehost/2016/9/13/225985a6-c1ad-4ff6-9a2d-fc33a69372c6.jpg",
        "https://pawarsupermall.com/images/homepersonal.jpg",
    ],
    "cleaning-household": [
        "https://africaforinvestors.com/media/opportunity/washing-liquids-with-sponges.webp",
        "https://www.woodfloordoctor.com/wp-content/uploads/2017/08/dish-soap-and-water-wood-floors.jpg",
        "https://cdn.tgdd.vn/hoi-dap/1366106/20-cach-diet-kien-tai-nha-tranh-chui-vao-cac-thiet-bi-dien15.jpg",
        "https://kitchen.sayidaty.net/uploads/small/73/73d73834f3c106d500aecae8c710fb6d_w750_h500.jpeg",
        "https://assets.yourlifechoices.com.au/2025/09/24170835/image-393.png",
        "https://i.blogs.es/37ebcb/lavado-de-liquidos-con-esponjas/1200_900.jpeg",
        "https://images.unsplash.com/photo-1563453392212-326f5e854473?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://www.ammonnews.net/image.php?size=xxlarge&token=aa833d64c2710f446552be7f6c36f7d3",
        "https://migrostoptanstr01.blob.core.windows.net/toptanimgsscale/11_72.jpg",
        "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&fm=jpg&q=80&w=1200",
    ],
    "mobile-accessories": [
        "https://mdb.ad-hoc-news.de/bild/bild-2765924_1920_1080.webp",
        "https://acf.geeknetic.es/imagenes/auto/25/08/22/uuo-los-mejores-cargadores-gan-carga-rapida-por-usb-para-todos-tus-dispositivos.png",
        "https://images.olx.com.pk/thumbnails/629775890-400x300.jpeg",
        "https://img.tvcmall.com/dynamic/uploads/details/740x740_6632001150A-1.webp",
        "https://image.msscdn.net/thumbnails/images/prd_img/20240116/3798118/detail_3798118_17053896127391_big.jpg?w=1200",
        "https://images.unsplash.com/photo-1614399113305-a127bb2ca893?auto=format&blend=000000&blend-alpha=10&blend-mode=normal&blend-w=1&crop=faces%2Cedges&fit=crop&h=630&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzAzMzg0NzY3fA&ixlib=rb-4.0.3&mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-align=top%2Cleft&mark-pad=50&mark-w=64&q=60&w=1200",
        "https://qpr.tn/cdn/shop/files/WhatsAppImage2026-07-22at18.50.39.jpg?v=1784742718&width=940",
        "https://euromalin.fr/images/posts/accessoires-tech-moins-30-euros.webp",
        "https://image.biccamera.com/img/00000012852147_A07.jpg?sr.dh=600&sr.dw=600&sr.jqh=60&sr.mat=1",
        "https://cdn.salla.sa/Orbp/a8f1aa39-d395-4876-b007-19247fbd317a-500x500-5qTi4qlpJyEHaBhpgsNGuXj4mxCrTny1ZjAvnu05.png",
    ],
    "clothing-men": [
        "https://funnelbuilder.sgp1.cdn.digitaloceanspaces.com/01KSFMF57ECXBGEKY16YAMZEYC.png",
        "https://www.moumachi.com.bd/images/listings/66015/business/20264-saints-banner-image.png",
        "https://e2simages.excess2sell.com/images/pviews/globuapmeme1755847061984_1755847062_view1.jpg",
        "https://www.uniqlo.com/id/en/news/sp/topics/2024072501/img/mimg_1_l.jpg",
        "https://i5.walmartimages.com/seo/Atasi-Solid-Mens-Hooded-Kurta-Full-Sleeve-Cotton-Tshirt-Regular-Fit-Ethnic-Wear_7354784f-54ed-45e0-afb1-f37b80b4d8e7.10e42e7683b807baefd181905670a8c4.jpeg",
        "https://down-id.img.susercontent.com/file/id-11134207-7r98p-lrwp9rddyi3ra9",
        "https://harvaa.in/cdn/shop/collections/photiu-2025-07-18_00-49-52-948.jpg?v=1752785454",
        "https://images.squarespace-cdn.com/content/v1/6956f9e466f79e7751896f4d/d2fb2c76-35fb-460e-a719-b7f1ff7f7fe1/B2354E34-C2F2-4B5B-A960-95CF771AA8FE.png",
        "https://kavyastyleplus.com/cdn/shop/files/Pursuite_20Iho_20F_20163_20Menology_20Mens_20Tshirts_20_281_29.jpg?v=1733212919",
        "https://kavyastyleplus.com/cdn/shop/files/Hoodies_20Code_20138_20Momentum_20Mens_20Tshirts_20_281_29.jpg?v=1732274373",
    ],
    "clothing-women": [
        "https://images.meesho.com/images/products/625818218/n41gt_512.webp?width=512",
        "https://www.unnatisilks.com/cdn/shop/articles/Untitled-1.jpg?v=1655286856&width=1200",
        "https://static.langimg.com/photo/imgsize-2081305%2Cmsid-128596109/navbharat-times.jpg",
        "https://images.meesho.com/images/products/707279820/thcsh_512.webp?width=512",
        "https://images.meesho.com/images/products/660609932/c1uym_512.webp?width=512",
        "https://images.meesho.com/images/products/714324618/zzged_512.webp?width=512",
        "https://rukminim3.flixcart.com/image/1114/972/xif0q/kurta/z/2/e/m-erlgsp01-maphaz-original-imahjw8fzzgsnuum.jpeg?crop=false&q=60",
        "https://images.meesho.com/images/products/716002197/oevt0_512.webp?width=512",
        "https://images.meesho.com/images/products/629752301/uahk4_512.webp?width=512",
        "https://images.meesho.com/images/products/625523628/kxoa0_512.jpg",
    ],
    "medicines": [
        "https://media04.rheinische-anzeigenblaetter.de/article/0001/01/01/4/1103554_XXL.jpg",
        "https://partoo-storelocator-medias.s3.eu-west-1.amazonaws.com/production/giphar/750593/111dd8f5-4a6e-4dfb-a267-c93bdc48ee41.JPG",
        "https://www.medical-confort.fr/media/images/upload/trousse-de-premiers-secours-medical-confort-lorient-lanester-ploemeur-1.png",
        "https://images.apollo247.in/pub/media/catalog/product/a/p/apf0003_1_2.jpg?tr=q-80",
        "https://geerdink.cl/cdn/shop/files/botiquin-imagen.png?crop=center&height=1200&v=1711461355&width=1200",
        "https://www.widforss.fi/_next/image?q=75&url=https%3A%2F%2Fwidforss.centracdn.net%2Fclient%2Fdynamic%2Fimages%2F26094_2032bf05a9-full.jpg&w=1730",
        "https://imagedelivery.net/dF1ylxvYlfOX5AA3mUQ_MA/0910be24-918f-45be-e342-e24fe00f6600/public",
        "https://cdn11.bigcommerce.com/s-c0xstle2uw/images/stencil/1280x1280/products/557/828/A004978__12180.1674668870.png?c=1",
        "https://www.widforss.no/_next/image?q=75&url=https%3A%2F%2Fwidforss.centracdn.net%2Fclient%2Fdynamic%2Fimages%2F26098_dc79260145-full.jpg&w=1440",
        "https://aptahospitalar.com.br/templates/yootheme/cache/89/47-896e0533.jpeg",
    ],
    "fresh-fruits": [
        "https://static.wixstatic.com/media/a0b12f_f500dbe776d449999b0a9bf859513fea~mv2.jpg/v1/fill/w_2500%2Ch_1013%2Cal_c/a0b12f_f500dbe776d449999b0a9bf859513fea~mv2.jpg",
        "https://www.annahar.com/Assets/ContentPhotos/Photos/1632778035320_120041.webp?height=805&mode=crop&scale=both&width=1416",
        "https://images.unsplash.com/photo-1674212466654-fccc10a1b594?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://cdn.shopify.com/s/files/1/1871/2763/articles/b3.jpg?v=1491504536",
        "https://mms.img.susercontent.com/vn-11134513-7r98o-lsvauzfiptp5b4%40resize_ss1242x600%21%40crop_w1242_h600_cT",
        "https://www.krushiworld.com/category-images/fresh-fruits.png",
        "https://static.africa-press.net/burkina/sites/42/2022/03/img-623cb3aaea0a0.jpg",
        "https://grafik2308.de/Nahrung/Gesundes/Obst/Auswahl_F/Fruechteauswahl/Fruechte%20006.jpg",
        "https://images.unsplash.com/photo-1716141458506-af5fe16bda11?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://images.unsplash.com/photo-1610768671751-fe7dc587cc9d?auto=format&fit=crop&fm=jpg&q=80&w=1200",
    ],
    "fresh-vegetables": [
        "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&fm=jpg&q=80&w=1200",
        "https://brainmd.com/cdn/shop/articles/Leafy-Greens-1_3b8b3b95-52e6-4071-8c13-ddbf684244bc.jpg?v=1767817351",
        "https://images.news.ru/2025/11/11/B32r8PZioK8A62Z0YsCwFYkHEflWqeXJSLOB2WpJ_780.png",
        "https://static.mooimom.id/media/ck-uploads/2021/11/12/img_8907.JPG",
        "https://www.culinar.ro/uploads/modules/news/0/2016/4/16/27507/fdb_1460790466_001.jpg",
        "https://tadayasai.com/upload/save_image/0316131128_641296f0ced64.jpg",
        "https://fruitabella.com.au/cdn/shop/products/image_a4765737-f6bf-4475-915e-1da512cf834b_530x%402x.jpg?v=1586776078",
        "https://cdn.shopify.com/s/files/1/0023/7722/0143/files/2023-09-06b_p3_Blog_image_fresh_vs_powdered_vegetables_480x480.png?v=1694038545",
        "https://www.nourishmentforlife.org/media/images/vegetables.jpg",
        "https://review-shopping.c.yimg.jp/images/y-sf_1017731/9d718dde-2793-42a3-9505-e16c3de67c93.jpeg",
    ],
}

DEMO_ROLES = [
    ('DEMO_ADMIN_EMAIL', 'DEMO_ADMIN_PASSWORD', 'admin@bazar.local', 'BAZAR Demo Admin', 'admin'),
    ('DEMO_SELLER_EMAIL', 'DEMO_SELLER_PASSWORD', 'demo-grocery@bazar.local', 'Demo Seller', 'seller'),
    ('DEMO_CUSTOMER_EMAIL', 'DEMO_CUSTOMER_PASSWORD', 'customer@bazar.local', 'Demo Customer', 'customer'),
]


class Command(BaseCommand):
    help = 'Seed essential categories for BAZAR marketplace'

    @staticmethod
    def _cloudinary_assets(api):
        """Load demo asset IDs in pages so restarts avoid one lookup per image."""
        public_ids = set()
        next_cursor = None
        try:
            while True:
                response = api.resources(
                    resource_type='image', type='upload',
                    prefix='media/bazar-demo/', max_results=500,
                    next_cursor=next_cursor,
                )
                public_ids.update(
                    asset.get('public_id') for asset in response.get('resources', [])
                    if asset.get('public_id')
                )
                next_cursor = response.get('next_cursor')
                if not next_cursor:
                    return public_ids
        except Exception:
            return None

    @staticmethod
    def _sync_cloudinary_asset(api, uploader, image_url, public_id, known_assets=None):
        cloudinary_public_id = f'media/{public_id}'
        if known_assets is not None and cloudinary_public_id in known_assets:
            return public_id
        if known_assets is None:
            try:
                api.resource(cloudinary_public_id, resource_type='image')
            except Exception:
                uploader.upload(
                    image_url,
                    public_id=cloudinary_public_id,
                    resource_type='image',
                )
        else:
            uploader.upload(
                image_url,
                public_id=cloudinary_public_id,
                resource_type='image',
            )
            known_assets.add(cloudinary_public_id)
        return public_id

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
            api = None

        known_assets = self._cloudinary_assets(api) if cloudinary_enabled else None

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
            if cloudinary_enabled:
                for image_field, source_key, folder in (
                    ('banner', 'banner_image', 'shop-banners'),
                    ('logo', 'logo_image', 'shop-logos'),
                ):
                    if not shop_data.get(source_key):
                        continue
                    image_url = (
                        f"https://images.unsplash.com/{shop_data[source_key]}"
                        '?auto=format&fit=crop&crop=entropy&fm=jpg&q=85&w=1400&h=700'
                    )
                    public_id = f'bazar-demo/{folder}/{shop.slug}'
                    try:
                        self._sync_cloudinary_asset(
                            api, uploader, image_url, public_id, known_assets,
                        )
                        setattr(shop, image_field, public_id)
                        shop.save(update_fields=[image_field])
                    except Exception as exc:
                        self.stderr.write(self.style.WARNING(
                            f'Could not sync demo {image_field} for {shop.name}: {exc}'
                        ))
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
                if not cloudinary_enabled:
                    continue
                try:
                    image_url = CATALOG_IMAGE_URLS[category_slug][index - 1]
                    public_id = f'bazar-demo/catalog-v2/{shop.slug}-{product.slug}'
                    self._sync_cloudinary_asset(
                        api, uploader, image_url, public_id, known_assets,
                    )
                    ProductImage.objects.update_or_create(
                        product=product, order=0,
                        defaults={
                            'image': public_id,
                            'alt_text': f'{name} — product photo',
                        },
                    )
                except Exception as exc:
                    self.stderr.write(self.style.WARNING(
                        f'Could not sync product photo for {name}: {exc}'
                    ))
