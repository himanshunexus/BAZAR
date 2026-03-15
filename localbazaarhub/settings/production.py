"""
Production settings for BAZAR.
"""

import dj_database_url

from decouple import Csv, config

from .base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# ──────────────────────────────────────
# Database – PostgreSQL via DATABASE_URL
# ──────────────────────────────────────

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
    )
}

# ──────────────────────────────────────
# Static files – WhiteNoise
# ──────────────────────────────────────
# Use CompressedStaticFilesStorage (NOT ManifestStaticFilesStorage)
# ManifestStaticFilesStorage crashes if any CSS/JS has a dangling
# reference. Compressed-only is safe and still serves gzip+brotli.

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# ──────────────────────────────────────
# Security
# ──────────────────────────────────────
# Render (and Railway) terminate SSL at the proxy, so Django never
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

# CSRF trusted origins — list every production domain explicitly.
# Wildcards like https://*.onrender.com are NOT supported by Django.
# Set this env var to your actual Render URL, e.g.:
#   CSRF_TRUSTED_ORIGINS=https://localbazaarhub.onrender.com
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://localhost',
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
