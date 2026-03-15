#!/usr/bin/env bash
# ──────────────────────────────────────
# LocalBazaarHub — Build Script
# Run before deployment to install deps,
# apply migrations, and collect static files.
# ──────────────────────────────────────
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete."
