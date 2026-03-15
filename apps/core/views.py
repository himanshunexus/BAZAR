from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, render

from apps.products.models import Product
from apps.shops.models import Category, Shop
from apps.shops.services import get_cities


def home(request):
    """Homepage – featured shops, categories, city selector."""
    featured_shops = (
        Shop.objects
        .filter(is_active=True, is_verified=True, is_featured=True)
        .select_related('category')[:8]
    )
    categories = Category.objects.filter(parent__isnull=True)[:12]
    cities = get_cities()[:20]
    recent_shops = (
        Shop.objects
        .filter(is_active=True, is_verified=True)
        .select_related('category')
        .annotate(avg_rating=Avg('reviews__rating'))[:12]
    )
    context = {
        'featured_shops': featured_shops,
        'categories': categories,
        'cities': cities,
        'recent_shops': recent_shops,
    }
    return render(request, 'core/home.html', context)


def city_select(request):
    """City / pincode selection page."""
    cities = get_cities()
    return render(request, 'core/city_select.html', {'cities': cities})


def category_page(request, slug):
    """Browse shops by category."""
    category = get_object_or_404(Category, slug=slug)
    shops = (
        Shop.objects
        .filter(is_active=True, is_verified=True, category=category)
        .select_related('category')
        .annotate(avg_rating=Avg('reviews__rating'))
    )
    city = request.GET.get('city', '')
    if city:
        shops = shops.filter(city__iexact=city)

    paginator = Paginator(shops, 12)
    page = paginator.get_page(request.GET.get('page'))
    context = {
        'category': category,
        'shops': page,
        'current_city': city,
    }
    return render(request, 'core/category_page.html', context)


def search(request):
    """Full-text search across shops and products."""
    query = request.GET.get('q', '').strip()
    shops = Shop.objects.none()
    products = Product.objects.none()

    if query:
        # Simple search using Q objects (works with SQLite and PostgreSQL)
        shops = (
            Shop.objects
            .filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(city__icontains=query),
                is_active=True, is_verified=True,
            )
            .select_related('category')[:20]
        )
        products = (
            Product.objects
            .filter(
                Q(name__icontains=query) | Q(description__icontains=query),
                is_active=True, shop__is_active=True,
            )
            .select_related('shop', 'category')
            .prefetch_related('images')[:20]
        )

    context = {
        'query': query,
        'shops': shops,
        'products': products,
    }
    if request.htmx:
        return render(request, 'core/partials/search_results.html', context)
    return render(request, 'core/search.html', context)
