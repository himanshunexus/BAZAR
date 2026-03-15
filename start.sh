#!/usr/bin/env bash
set -o errexit

gunicorn localbazaarhub.wsgi:application --bind 0.0.0.0:$PORT
