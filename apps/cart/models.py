import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        PROCESSING = 'processing', 'Processing'
        READY_FOR_PICKUP = 'ready_for_pickup', 'Ready for pickup'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders'
    )
    shop = models.ForeignKey(
        'shops.Shop', on_delete=models.CASCADE, related_name='orders'
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField(blank=True)
    payment_method = models.CharField(
        max_length=20,
        choices=[('pay_at_shop', 'Pay at shop')],
        default='pay_at_shop',
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"

    def get_whatsapp_url(self):
        from urllib.parse import quote

        phone = ''.join(filter(str.isdigit, self.shop.whatsapp_phone or self.shop.contact_phone))
        if not phone:
            return ''

        item_lines = '\n'.join(
            f'- {item.product_name} x {item.quantity}'
            for item in self.items.all()
        )
        message = (
            f"Hello {self.shop.name}, I placed BAZAR order {str(self.order_id)[:8]}.\n"
            f"{item_lines}\n"
            f"Total: ₹{self.total_amount}\n"
            f"Customer: {self.customer_name} ({self.customer_phone})\n"
            'Please contact me to arrange shop pickup.'
        )
        return f'https://wa.me/{phone}?text={quote(message)}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL, null=True
    )
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    @property
    def subtotal(self):
        return self.product_price * self.quantity
