"""
Production settings for BAZAR.
"""

import os

from decouple import Csv, config

from .base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# ──────────────────────────────────────
# Database – SQLite (Render free web services have ephemeral storage)
# ──────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    },
}

# ──────────────────────────────────────
# Static files – WhiteNoise
# ──────────────────────────────────────
# Use CompressedStaticFilesStorage (NOT ManifestStaticFilesStorage)
# ManifestStaticFilesStorage crashes if any CSS/JS has a dangling
# reference. Compressed-only is safe and still serves gzip+brotli.

STORAGES['staticfiles'] = {  # noqa: F405
    'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
}

# ──────────────────────────────────────
# Security
# ──────────────────────────────────────
# Render terminates SSL at the proxy, so Django never
# sees an HTTPS request directly. SECURE_SSL_REDIRECT must be False
# or the proxy and Django enter an infinite 301 loop.
# The proxy header tells Django the original request was HTTPS.

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins — auto-detected from Render's RENDER_EXTERNAL_URL
# env var (set automatically by Render on every service), so no manual
# dashboard config is needed.  Falls back to CSRF_TRUSTED_ORIGINS env var
# if set, then to https://localhost as last resort.
_render_url = os.environ.get('RENDER_EXTERNAL_URL', '')
_default_origins = _render_url if _render_url else 'https://localhost'

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default=_default_origins,
    cast=Csv(),
)

# ──────────────────────────────────────
# Email (configure for production)
# ──────────────────────────────────────

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ──────────────────────────────────────
# Logging — console only, WARNING+ level
# ──────────────────────────────────────

LOGGING['root']['level'] = 'WARNING'  # noqa: F405
LOGGING['loggers']['django']['level'] = 'WARNING'  # noqa: F405
