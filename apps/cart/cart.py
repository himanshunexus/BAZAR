from decimal import Decimal
from apps.products.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    """Session-based shopping cart."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.display_price),
            }
        new_qty = self.cart[product_id]['quantity'] + quantity
        # Cap at available stock
        if product.stock is not None:
            new_qty = min(new_qty, product.stock)
        self.cart[product_id]['quantity'] = max(new_qty, 1)
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity <= 0:
                self.remove(product)
            else:
                # Cap at available stock
                if product.stock is not None:
                    quantity = min(quantity, product.stock)
                self.cart[product_id]['quantity'] = quantity
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        if CART_SESSION_KEY in self.session:
            del self.session[CART_SESSION_KEY]
        self.cart = {}
        self.save()

    def __iter__(self):
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids).prefetch_related('images')
        products_map = {str(p.id): p for p in products}

        # Remove items whose products no longer exist
        stale_ids = [pid for pid in product_ids if pid not in products_map]
        for pid in stale_ids:
            del self.cart[pid]
        if stale_ids:
            self.save()

        for product_id, item in self.cart.items():
            item_copy = item.copy()
            item_copy['product'] = products_map[product_id]
            item_copy['price'] = Decimal(item_copy['price'])
            item_copy['total_price'] = item_copy['price'] * item_copy['quantity']
            yield item_copy

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
