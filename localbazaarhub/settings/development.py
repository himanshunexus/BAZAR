"""
Development settings for BAZAR.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['*']

# ──────────────────────────────────────
# Database – SQLite for local dev
# ──────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

# ──────────────────────────────────────
# Debug Toolbar (optional — only if installed)
# ──────────────────────────────────────

try:
    import debug_toolbar  # noqa: F401

    INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass

# ──────────────────────────────────────
# Email – Console backend for dev
# ──────────────────────────────────────

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ──────────────────────────────────────
# WhiteNoise for static in dev too
# ──────────────────────────────────────

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# ──────────────────────────────────────
# Logging — more verbose in dev
# ──────────────────────────────────────

LOGGING['root']['level'] = 'INFO'  # noqa: F405
LOGGING['loggers']['django']['level'] = 'INFO'  # noqa: F405
