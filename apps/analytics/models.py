from django.db import models


class ShopAnalytics(models.Model):
    shop = models.ForeignKey(
        'shops.Shop', on_delete=models.CASCADE, related_name='analytics'
    )
    date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    product_views = models.PositiveIntegerField(default=0)
    whatsapp_clicks = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Shop Analytics'
        unique_together = ['shop', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.shop.name} - {self.date}"
