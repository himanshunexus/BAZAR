#!/usr/bin/env bash
set -o errexit

exec gunicorn localbazaarhub.wsgi:application \
    --bind "0.0.0.0:${PORT:-10000}" \
    --timeout 120 \
    --preload
