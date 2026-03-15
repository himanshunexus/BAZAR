from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE, related_name='children'
    )
    icon = models.CharField(max_length=50, blank=True, help_text='Tailwind icon class or emoji')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:category', kwargs={'slug': self.slug})


class Shop(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shop'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='shops'
    )
    address = models.TextField()
    city = models.CharField(max_length=100, db_index=True)
    pincode = models.CharField(max_length=10, db_index=True)
    state = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=15)
    whatsapp_phone = models.CharField(max_length=15, blank=True)
    logo = models.ImageField(upload_to='shops/logos/', blank=True)
    banner = models.ImageField(upload_to='shops/banners/', blank=True)
    opening_hours = models.CharField(max_length=200, blank=True, help_text='e.g. Mon-Sat 9AM-8PM')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['city', 'pincode']),
            models.Index(fields=['category']),
            models.Index(fields=['is_verified', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness
            qs = Shop.objects.filter(slug=self.slug)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                self.slug = f"{self.slug}-{self.pincode}"
        if not self.whatsapp_phone:
            self.whatsapp_phone = self.contact_phone
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shops:detail', kwargs={'slug': self.slug})

    def get_whatsapp_url(self):
        phone = self.whatsapp_phone.lstrip('+').replace(' ', '')
        return f"https://wa.me/{phone}?text=Hello%20I%20found%20your%20shop%20on%20BAZAR"

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()
