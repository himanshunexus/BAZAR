from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class ProductCategory(models.Model):
    """Product-level categories (e.g. Rice, Dal, Shampoo, Cables)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE, related_name='children'
    )

    class Meta:
        verbose_name_plural = 'Product Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    shop = models.ForeignKey(
        'shops.Shop', on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=30, blank=True, help_text='e.g. kg, piece, litre')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['shop', 'slug']
        indexes = [
            models.Index(fields=['shop', 'is_active']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness within shop
            qs = Product.objects.filter(shop=self.shop, slug=self.slug)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            counter = 1
            original = self.slug
            while qs.exists():
                self.slug = f"{original}-{counter}"
                qs = Product.objects.filter(shop=self.shop, slug=self.slug)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={
            'shop_slug': self.shop.slug,
            'slug': self.slug
        })

    @property
    def display_price(self):
        return self.discounted_price if self.discounted_price else self.price

    @property
    def discount_percent(self):
        if self.discounted_price and self.price > 0:
            return round((1 - self.discounted_price / self.price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    def get_whatsapp_url(self):
        phone = self.shop.whatsapp_phone.lstrip('+').replace(' ', '')
        text = f"Hello, I saw {self.name} (₹{self.display_price}) on BAZAR"
        from urllib.parse import quote
        return f"https://wa.me/{phone}?text={quote(text)}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80}
    )
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"
