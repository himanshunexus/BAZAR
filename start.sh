#!/usr/bin/env bash
# ──────────────────────────────────────
# LocalBazaarHub — Start Script
# Launches the Gunicorn production server.
# ──────────────────────────────────────
set -o errexit

exec gunicorn localbazaarhub.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${WEB_CONCURRENCY:-3} \
    --timeout 120
