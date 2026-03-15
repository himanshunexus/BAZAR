from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.products.models import Product
from apps.shops.models import Shop

from .cart import Cart
from .models import Order, OrderItem


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)
    messages.success(request, f'"{product.name}" added to cart.')
    if request.htmx:
        return render(request, 'cart/partials/cart_icon.html', {'cart': cart})
    return redirect('cart:detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 0))
    cart.update_quantity(product, quantity)
    if request.htmx:
        return render(request, 'cart/cart_detail.html', {'cart': cart})
    return redirect('cart:detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'"{product.name}" removed from cart.')
    if request.htmx:
        return render(request, 'cart/cart_detail.html', {'cart': cart})
    return redirect('cart:detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not all([name, phone, address]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'cart/checkout.html', {'cart': cart})

        # Group cart items by shop
        items_by_shop = defaultdict(list)
        for item in cart:
            shop = item['product'].shop
            items_by_shop[shop].append(item)

        try:
            with transaction.atomic():
                created_orders = []
                for shop, items in items_by_shop.items():
                    total = sum(i['total_price'] for i in items)
                    order = Order.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        shop=shop,
                        customer_name=name,
                        customer_phone=phone,
                        customer_address=address,
                        payment_method='cod',
                        total_amount=total,
                    )
                    for item in items:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            product_name=item['product'].name,
                            product_price=item['price'],
                            quantity=item['quantity'],
                        )
                        # Decrement stock
                        product = item['product']
                        if product.stock is not None:
                            product.stock = max(0, product.stock - item['quantity'])
                            product.save(update_fields=['stock'])
                    created_orders.append(order)

                cart.clear()
                return redirect('cart:order_success')

        except Exception:
            messages.error(request, 'Something went wrong placing your order. Please try again.')
            return render(request, 'cart/checkout.html', {'cart': cart})

    return render(request, 'cart/checkout.html', {'cart': cart})


def order_success(request):
    return render(request, 'cart/order_success.html')


# ──────────────────────────────────────
# Seller Order Management
# ──────────────────────────────────────

@login_required
def seller_orders(request):
    """Seller views all orders for their shop."""
    shop = get_object_or_404(Shop, owner=request.user)
    orders = Order.objects.filter(shop=shop).prefetch_related('items').order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)

    paginator = Paginator(orders, 20)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        'shop': shop,
        'orders': page,
        'status_choices': Order.Status.choices,
        'current_status': status_filter,
    }
    return render(request, 'seller/orders.html', context)


@login_required
def seller_order_detail(request, order_id):
    """Seller views/updates a single order."""
    shop = get_object_or_404(Shop, owner=request.user)
    order = get_object_or_404(Order, order_id=order_id, shop=shop)

    if request.method == 'POST':
        new_status = request.POST.get('status', '')
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save(update_fields=['status', 'updated_at'])
            messages.success(request, f'Order status updated to {order.get_status_display()}.')
        return redirect('cart:seller_order_detail', order_id=order.order_id)

    context = {
        'shop': shop,
        'order': order,
        'items': order.items.all(),
        'status_choices': Order.Status.choices,
    }
    return render(request, 'seller/order_detail.html', context)
