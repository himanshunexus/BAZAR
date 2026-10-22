#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-localbazaarhub.settings.production}"

python manage.py migrate --noinput
python manage.py seed_data

exec gunicorn localbazaarhub.wsgi:application \
    --bind "0.0.0.0:${PORT:-10000}" \
    --workers 1 \
    --timeout 120
