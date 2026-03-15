from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F
from django.shortcuts import get_object_or_404, redirect, render

from apps.analytics.models import ShopAnalytics
from apps.cart.models import Order

from .forms import ShopForm
from .models import Category, Shop


def shop_list(request):
    """List shops filtered by city, pincode, or category."""
    shops = Shop.objects.filter(is_active=True, is_verified=True).select_related('category', 'owner')
    city = request.GET.get('city', '').strip()
    pincode = request.GET.get('pincode', '').strip()
    category_slug = request.GET.get('category', '').strip()

    if city:
        shops = shops.filter(city__iexact=city)
    if pincode:
        shops = shops.filter(pincode=pincode)
    if category_slug:
        shops = shops.filter(category__slug=category_slug)

    shops = shops.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
    )

    categories = Category.objects.filter(parent__isnull=True)
    context = {
        'shops': shops,
        'categories': categories,
        'current_city': city,
        'current_pincode': pincode,
        'current_category': category_slug,
    }

    if request.htmx:
        return render(request, 'shops/partials/shop_cards.html', context)
    return render(request, 'shops/shop_list.html', context)


def shop_detail(request, slug):
    """Shop detail with products."""
    shop = get_object_or_404(
        Shop.objects.select_related('owner', 'category'),
        slug=slug, is_active=True
    )
    products = shop.products.filter(is_active=True).prefetch_related('images')
    reviews = shop.reviews.select_related('user')[:10]
    avg_rating = shop.reviews.aggregate(avg=Avg('rating'))['avg']

    # Track analytics
    analytics, _ = ShopAnalytics.objects.get_or_create(
        shop=shop, date=date.today()
    )
    ShopAnalytics.objects.filter(pk=analytics.pk).update(views=F('views') + 1)

    context = {
        'shop': shop,
        'products': products,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'shops/shop_detail.html', context)


@login_required
def shop_create(request):
    """Create shop – seller only."""
    if not request.user.is_seller:
        messages.error(request, 'You need a seller account to create a shop.')
        return redirect('accounts:register_seller')
    if hasattr(request.user, 'shop'):
        return redirect('shops:dashboard')

    # Auto-seed categories if the table is empty (safety net for fresh DBs)
    if not Category.objects.exists():
        _seed_shop_categories()

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.is_verified = True
            shop.save()
            messages.success(request, 'Shop created! Add your products now.')
            return redirect('shops:dashboard')
    else:
        form = ShopForm()
    return render(request, 'shops/shop_form.html', {'form': form, 'title': 'Create Your Shop'})


def _seed_shop_categories():
    """One-time inline seed if build.sh seed_data was skipped."""
    CATS = [
        {'name': 'Grocery & Kirana', 'slug': 'grocery', 'icon': '\U0001f6d2', 'order': 1},
        {'name': 'Electronics', 'slug': 'electronics', 'icon': '\U0001f4f1', 'order': 2},
        {'name': 'Clothing & Fashion', 'slug': 'clothing', 'icon': '\U0001f457', 'order': 3},
        {'name': 'Pharmacy', 'slug': 'pharmacy', 'icon': '\U0001f48a', 'order': 4},
        {'name': 'Bakery & Sweets', 'slug': 'bakery', 'icon': '\U0001f370', 'order': 5},
        {'name': 'Fruits & Vegetables', 'slug': 'fruits-vegetables', 'icon': '\U0001f96c', 'order': 6},
        {'name': 'Hardware & Tools', 'slug': 'hardware', 'icon': '\U0001f527', 'order': 7},
        {'name': 'Stationery & Books', 'slug': 'stationery', 'icon': '\U0001f4da', 'order': 8},
        {'name': 'Beauty & Salon', 'slug': 'beauty', 'icon': '\U0001f487', 'order': 9},
        {'name': 'Restaurant & Food', 'slug': 'restaurant', 'icon': '\U0001f37d\ufe0f', 'order': 10},
        {'name': 'Home & Kitchen', 'slug': 'home-kitchen', 'icon': '\U0001f3e0', 'order': 11},
        {'name': 'Sports & Fitness', 'slug': 'sports', 'icon': '\u26bd', 'order': 12},
    ]
    for data in CATS:
        Category.objects.get_or_create(slug=data['slug'], defaults=data)


@login_required
def shop_edit(request):
    """Edit shop – owner only."""
    shop = get_object_or_404(Shop, owner=request.user)
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop updated.')
            return redirect('shops:dashboard')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'shops/shop_form.html', {'form': form, 'title': 'Edit Shop'})


@login_required
def seller_dashboard(request):
    """Seller dashboard with analytics."""
    try:
        shop = Shop.objects.get(owner=request.user)
    except Shop.DoesNotExist:
        messages.info(request, 'Create your shop first to access the dashboard.')
        return redirect('shops:create')
    products = shop.products.all()[:10]
    total_products = shop.products.count()
    total_orders = Order.objects.filter(shop=shop).count()
    recent_reviews = shop.reviews.select_related('user')[:5]
    today_analytics, _ = ShopAnalytics.objects.get_or_create(
        shop=shop, date=date.today()
    )
    analytics_30 = ShopAnalytics.objects.filter(shop=shop).order_by('-date')[:30]

    context = {
        'shop': shop,
        'products': products,
        'total_products': total_products,
        'total_orders': total_orders,
        'recent_reviews': recent_reviews,
        'today_analytics': today_analytics,
        'analytics_history': analytics_30,
    }
    return render(request, 'seller/dashboard.html', context)


@login_required
def pdf_catalog(request):
    """Generate PDF catalog for seller's shop."""
    from django.http import HttpResponse
    from django.template.loader import render_to_string

    try:
        from weasyprint import HTML
    except (ImportError, OSError):
        return HttpResponse(
            'PDF generation is not available — WeasyPrint or its system libraries (pango, cairo) are missing.',
            status=503,
        )

    shop = get_object_or_404(Shop, owner=request.user)
    products = shop.products.filter(is_active=True).prefetch_related('images')

    html_string = render_to_string('shops/pdf_catalog.html', {
        'shop': shop,
        'products': products,
    })

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{shop.slug}-catalog.pdf"'
    return response
