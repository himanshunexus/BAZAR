from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    shop = models.ForeignKey(
        'shops.Shop', on_delete=models.CASCADE,
        null=True, blank=True, related_name='reviews'
    )
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE,
        null=True, blank=True, related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        target = self.shop or self.product
        return f"Review by {self.user.email} on {target}"
