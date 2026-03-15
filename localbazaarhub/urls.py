from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# ──────────────────────────────────────
# Django Admin Branding
# ──────────────────────────────────────
admin.site.site_header = 'BAZAR Admin'
admin.site.site_title = 'BAZAR Admin Portal'
admin.site.index_title = 'Welcome to BAZAR Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('shops/', include('apps.shops.urls')),
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('platform-admin/', include('apps.platform_admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
