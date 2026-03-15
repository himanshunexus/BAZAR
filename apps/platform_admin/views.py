from datetime import timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.accounts.models import User
from apps.analytics.models import ShopAnalytics
from apps.cart.models import Order
from apps.products.models import Product, ProductCategory
from apps.reviews.models import Review
from apps.shops.models import Category, Shop

from .decorators import staff_required


# ──────────────────────────────────────
# Dashboard
# ──────────────────────────────────────

@staff_required
def dashboard(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    context = {
        'total_users': User.objects.count(),
        'total_sellers': User.objects.filter(is_seller=True).count(),
        'total_shops': Shop.objects.count(),
        'verified_shops': Shop.objects.filter(is_verified=True).count(),
        'pending_shops': Shop.objects.filter(is_verified=False, is_active=True).count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_revenue': Order.objects.filter(status='delivered').aggregate(s=Sum('total_amount'))['s'] or 0,
        'total_reviews': Review.objects.count(),
        'new_users_week': User.objects.filter(date_joined__gte=week_ago).count(),
        'new_shops_week': Shop.objects.filter(created_at__gte=week_ago).count(),
        'new_orders_week': Order.objects.filter(created_at__gte=week_ago).count(),
        'recent_shops': Shop.objects.select_related('owner', 'category').order_by('-created_at')[:5],
        'recent_orders': Order.objects.select_related('shop').order_by('-created_at')[:5],
        'recent_reviews': Review.objects.select_related('user', 'shop').order_by('-created_at')[:5],
    }
    return render(request, 'platform_admin/dashboard.html', context)


# ──────────────────────────────────────
# Shop Management
# ──────────────────────────────────────

@staff_required
def shop_list(request):
    shops = Shop.objects.select_related('owner', 'category').all()

    status = request.GET.get('status', '')
    if status == 'verified':
        shops = shops.filter(is_verified=True)
    elif status == 'pending':
        shops = shops.filter(is_verified=False, is_active=True)
    elif status == 'suspended':
        shops = shops.filter(is_active=False)

    q = request.GET.get('q', '').strip()
    if q:
        shops = shops.filter(name__icontains=q)

    shops = shops.order_by('-created_at')
    paginator = Paginator(shops, 20)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        'shops': page,
        'current_status': status,
        'q': q,
    }
    return render(request, 'platform_admin/shops.html', context)


@staff_required
@require_POST
def shop_action(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    action = request.POST.get('action', '')

    if action == 'verify':
        shop.is_verified = True
        shop.is_active = True
        shop.save(update_fields=['is_verified', 'is_active'])
        messages.success(request, f'"{shop.name}" verified.')
    elif action == 'suspend':
        shop.is_active = False
        shop.save(update_fields=['is_active'])
        messages.warning(request, f'"{shop.name}" suspended.')
    elif action == 'activate':
        shop.is_active = True
        shop.save(update_fields=['is_active'])
        messages.success(request, f'"{shop.name}" activated.')
    elif action == 'feature':
        shop.is_featured = not shop.is_featured
        shop.save(update_fields=['is_featured'])
        label = 'featured' if shop.is_featured else 'unfeatured'
        messages.success(request, f'"{shop.name}" {label}.')

    return redirect(request.POST.get('next', 'platform_admin:shops'))


# ──────────────────────────────────────
# Product Moderation
# ──────────────────────────────────────

@staff_required
def product_list(request):
    products = Product.objects.select_related('shop', 'category').all()

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(name__icontains=q)

    status = request.GET.get('status', '')
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)

    paginator = Paginator(products, 30)
    page = paginator.get_page(request.GET.get('page'))

    context = {'products': page, 'q': q, 'current_status': status}
    return render(request, 'platform_admin/products.html', context)


@staff_required
@require_POST
def product_action(request, pk):
    product = get_object_or_404(Product, pk=pk)
    action = request.POST.get('action', '')

    if action == 'disable':
        product.is_active = False
        product.save(update_fields=['is_active'])
        messages.warning(request, f'"{product.name}" disabled.')
    elif action == 'enable':
        product.is_active = True
        product.save(update_fields=['is_active'])
        messages.success(request, f'"{product.name}" enabled.')
    elif action == 'delete':
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" deleted.')

    return redirect('platform_admin:products')


# ──────────────────────────────────────
# User Management
# ──────────────────────────────────────

@staff_required
def user_list(request):
    users = User.objects.all()

    role = request.GET.get('role', '')
    if role == 'seller':
        users = users.filter(is_seller=True)
    elif role == 'customer':
        users = users.filter(is_seller=False, is_staff=False)
    elif role == 'staff':
        users = users.filter(is_staff=True)

    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(email__icontains=q)

    paginator = Paginator(users, 30)
    page = paginator.get_page(request.GET.get('page'))

    context = {'users': page, 'q': q, 'current_role': role}
    return render(request, 'platform_admin/users.html', context)


@staff_required
@require_POST
def user_action(request, pk):
    target = get_object_or_404(User, pk=pk)
    action = request.POST.get('action', '')

    if target.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Cannot modify superuser account.')
        return redirect('platform_admin:users')

    if action == 'block':
        target.is_active = False
        target.save(update_fields=['is_active'])
        messages.warning(request, f'{target.email} blocked.')
    elif action == 'unblock':
        target.is_active = True
        target.save(update_fields=['is_active'])
        messages.success(request, f'{target.email} unblocked.')
    elif action == 'verify_seller':
        target.is_seller = True
        target.is_verified = True
        target.save(update_fields=['is_seller', 'is_verified'])
        messages.success(request, f'{target.email} verified as seller.')

    return redirect('platform_admin:users')


# ──────────────────────────────────────
# Review Moderation
# ──────────────────────────────────────

@staff_required
def review_list(request):
    reviews = Review.objects.select_related('user', 'shop', 'product').all()

    paginator = Paginator(reviews, 30)
    page = paginator.get_page(request.GET.get('page'))

    context = {'reviews': page}
    return render(request, 'platform_admin/reviews.html', context)


@staff_required
@require_POST
def review_action(request, pk):
    review = get_object_or_404(Review, pk=pk)
    action = request.POST.get('action', '')

    if action == 'delete':
        review.delete()
        messages.success(request, 'Review deleted.')

    return redirect('platform_admin:reviews')


# ──────────────────────────────────────
# Category Management
# ──────────────────────────────────────

@staff_required
def category_list(request):
    shop_categories = Category.objects.all()
    product_categories = ProductCategory.objects.all()

    context = {
        'shop_categories': shop_categories,
        'product_categories': product_categories,
    }
    return render(request, 'platform_admin/categories.html', context)


@staff_required
@require_POST
def category_create(request):
    cat_type = request.POST.get('type', 'shop')
    name = request.POST.get('name', '').strip()
    if not name:
        messages.error(request, 'Category name is required.')
        return redirect('platform_admin:categories')

    if cat_type == 'product':
        ProductCategory.objects.create(name=name)
        messages.success(request, f'Product category "{name}" created.')
    else:
        Category.objects.create(name=name)
        messages.success(request, f'Shop category "{name}" created.')

    return redirect('platform_admin:categories')


@staff_required
@require_POST
def category_delete(request, pk):
    cat_type = request.POST.get('type', 'shop')
    if cat_type == 'product':
        obj = get_object_or_404(ProductCategory, pk=pk)
    else:
        obj = get_object_or_404(Category, pk=pk)
    name = obj.name
    obj.delete()
    messages.success(request, f'"{name}" deleted.')
    return redirect('platform_admin:categories')


# ──────────────────────────────────────
# Featured Shops
# ──────────────────────────────────────

@staff_required
def featured_shops(request):
    featured = Shop.objects.filter(is_featured=True).select_related('category')
    all_shops = Shop.objects.filter(is_active=True, is_verified=True, is_featured=False).select_related('category')

    context = {
        'featured': featured,
        'available_shops': all_shops,
    }
    return render(request, 'platform_admin/featured.html', context)


# ──────────────────────────────────────
# Analytics
# ──────────────────────────────────────

@staff_required
def analytics_page(request):
    # Shops per city (top 15)
    shops_by_city = (
        Shop.objects.filter(is_active=True)
        .values('city')
        .annotate(count=Count('id'))
        .order_by('-count')[:15]
    )

    # Products per category (top 15)
    products_by_category = (
        Product.objects
        .filter(category__isnull=False)
        .values('category__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:15]
    )

    # User growth — last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    users_by_day = (
        User.objects.filter(date_joined__gte=thirty_days_ago)
        .annotate(day=TruncDate('date_joined'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Orders by status
    orders_by_status = (
        Order.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'shops_by_city': list(shops_by_city),
        'products_by_category': list(products_by_category),
        'users_by_day': list(users_by_day),
        'orders_by_status': list(orders_by_status),
    }
    return render(request, 'platform_admin/analytics.html', context)
