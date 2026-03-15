from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from apps.analytics.models import ShopAnalytics
from apps.shops.models import Shop

from .filters import ProductFilter
from .forms import ProductForm, ProductImageFormSet
from .models import Product


def product_detail(request, shop_slug, slug):
    """Product detail page with WhatsApp button."""
    product = get_object_or_404(
        Product.objects.select_related('shop', 'category').prefetch_related('images', 'reviews'),
        shop__slug=shop_slug,
        slug=slug,
        is_active=True,
    )
    related = Product.objects.filter(
        shop=product.shop, is_active=True
    ).exclude(pk=product.pk)[:4]

    # Track product view analytics
    analytics, _ = ShopAnalytics.objects.get_or_create(
        shop=product.shop, date=date.today()
    )
    ShopAnalytics.objects.filter(pk=analytics.pk).update(product_views=F('product_views') + 1)

    context = {
        'product': product,
        'related_products': related,
        'images': product.images.all(),
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def product_list_seller(request):
    """Seller's product list manager."""
    shop = get_object_or_404(Shop, owner=request.user)
    products = shop.products.all()

    product_filter = ProductFilter(request.GET, queryset=products)
    paginator = Paginator(product_filter.qs, 20)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        'shop': shop,
        'products': page,
        'filter': product_filter,
    }
    return render(request, 'seller/product_list.html', context)


@login_required
def product_add(request):
    """Add product – seller only."""
    shop = get_object_or_404(Shop, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            formset.instance = product
            formset.save()
            messages.success(request, f'"{product.name}" added.')
            return redirect('products:seller_list')
    else:
        form = ProductForm()
        formset = ProductImageFormSet()
    return render(request, 'seller/product_form.html', {
        'form': form, 'formset': formset, 'title': 'Add Product',
    })


@login_required
def product_edit(request, pk):
    """Edit product – owner only."""
    product = get_object_or_404(Product, pk=pk, shop__owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'"{product.name}" updated.')
            return redirect('products:seller_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    return render(request, 'seller/product_form.html', {
        'form': form, 'formset': formset, 'title': 'Edit Product',
    })


@login_required
def product_delete(request, pk):
    """Delete product – owner only."""
    product = get_object_or_404(Product, pk=pk, shop__owner=request.user)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('products:seller_list')
    return render(request, 'seller/product_confirm_delete.html', {'product': product})


@login_required
def bulk_import(request):
    """Bulk import products via CSV."""
    shop = get_object_or_404(Shop, owner=request.user)
    if request.method == 'POST' and request.FILES.get('csv_file'):
        import csv
        import io
        from django.db import transaction

        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('products:bulk_import')

        decoded = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
        count = 0
        errors = []
        try:
            with transaction.atomic():
                for row_num, row in enumerate(reader, start=2):
                    name = row.get('name', '').strip()
                    if not name:
                        errors.append(f'Row {row_num}: Missing product name, skipped.')
                        continue
                    try:
                        price = float(row.get('price', 0) or 0)
                    except (ValueError, TypeError):
                        errors.append(f'Row {row_num}: Invalid price for "{name}", skipped.')
                        continue
                    try:
                        stock = int(row.get('stock', 0) or 0)
                    except (ValueError, TypeError):
                        stock = 0
                    disc_price = row.get('discounted_price', '').strip()
                    try:
                        disc_price = float(disc_price) if disc_price else None
                    except (ValueError, TypeError):
                        disc_price = None

                    Product.objects.create(
                        shop=shop,
                        name=name,
                        description=row.get('description', ''),
                        price=price,
                        discounted_price=disc_price,
                        stock=stock,
                        unit=row.get('unit', ''),
                    )
                    count += 1
        except Exception as e:
            messages.error(request, f'Import failed: {e}')
            return redirect('products:bulk_import')

        if errors:
            messages.warning(request, f'{count} products imported. {len(errors)} row(s) skipped.')
        else:
            messages.success(request, f'{count} products imported successfully.')
        return redirect('products:seller_list')
    return render(request, 'seller/bulk_import.html', {'shop': shop})
