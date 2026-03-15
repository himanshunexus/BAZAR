#!/usr/bin/env bash
# ──────────────────────────────────────
# BAZAR — Build Script
# Run before deployment to install deps,
# apply migrations, and collect static files.
# ──────────────────────────────────────
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

# WeasyPrint needs system C libraries (pango, cairo) that may be missing.
# Install it separately so a failure doesn't kill the entire build.
pip install WeasyPrint>=61.0 || echo "WARNING: WeasyPrint install failed — PDF generation will be disabled."

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding essential data..."
python manage.py seed_data

echo "Build complete."
