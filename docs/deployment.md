# LocalBazaarHub - Deployment Guide

## Local Development

```bash
# 1. Clone and setup
cd "BAZAR HUB"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. Run development server
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Seeding Data

After creating a superuser, go to http://127.0.0.1:8000/admin/ and:

1. **Add Categories** (Grocery, Electronics, Clothing, Pharmacy, etc.)
2. **Create a seller user** (set is_seller=True)
3. **Create a shop** linked to that seller
4. **Add products** to the shop
5. **Mark the shop as verified** so it appears in listings

## Deployment on Render

1. Push code to GitHub
2. Create a **New Web Service** on Render
3. Connect your repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn localbazaarhub.wsgi:application`
5. Add environment variables:
   - `SECRET_KEY` = (generate a strong key)
   - `DJANGO_SETTINGS_MODULE` = `localbazaarhub.settings.production`
   - `ALLOWED_HOSTS` = `your-app.onrender.com`
   - `DATABASE_URL` = (from Render PostgreSQL)
6. Add a **PostgreSQL** database from Render dashboard

## Deployment on Railway

1. Push code to GitHub
2. Create a **New Project** on Railway
3. Add **PostgreSQL** plugin
4. Connect your repository
5. Add environment variables:
   - `SECRET_KEY` = (generate a strong key)
   - `DJANGO_SETTINGS_MODULE` = `localbazaarhub.settings.production`
   - `ALLOWED_HOSTS` = `your-app.up.railway.app`
   - `DATABASE_URL` = (auto-provided by Railway PostgreSQL)
6. Deploy

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DJANGO_SETTINGS_MODULE` | Settings module path | Yes |
| `DATABASE_URL` | PostgreSQL connection URL | Yes (production) |
| `ALLOWED_HOSTS` | Comma-separated hostnames | Yes (production) |
| `RAZORPAY_KEY_ID` | Razorpay API key | Optional |
| `RAZORPAY_KEY_SECRET` | Razorpay API secret | Optional |
| `SECURE_SSL_REDIRECT` | HTTPS redirect (True/False) | Optional |

## Static & Media Files

- **Static files**: Served by WhiteNoise (included in middleware)
- **Media files**: For production, use an S3-compatible storage (Cloudflare R2, AWS S3)

## Quick Generate Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
